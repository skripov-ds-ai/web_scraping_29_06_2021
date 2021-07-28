import copy
import json
import re
from urllib.parse import quote

import scrapy
from scrapy.http import HtmlResponse

from instagram_scraper.items import InstagramScraperItem


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/"]
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    template_user_url = "/%s"
    post_getting_url = "/graphql/query/?query_hash=%s&variables=%s"
    post_query_hash = "8c2a529969ee035a5063f2fc8602a0fd"

    def __init__(self, login, password, user_to_parse, **kwargs):
        super().__init__(**kwargs)
        self.login = login
        self.enc_password = password
        self.user_to_parse = user_to_parse

    def parse(self, response: HtmlResponse, **kwargs):
        token = self.fetch_csrf_token(response.text)
        x_instagram_ajax = self.fetch_x_instagram_ajax(response.text)
        yield scrapy.FormRequest(
            url=self.login_url,
            method="POST",
            formdata={
                "username": self.login,
                "enc_password": self.enc_password,
            },
            headers={
                "X-CSRFToken": token,
                "x-ig-app-id": "936619743392459",
                "x-instagram-ajax": x_instagram_ajax,
            },
            callback=self.user_login,
        )

    def user_login(self, response: HtmlResponse):
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print("Json decode error")
            print(e)
            return
        except Exception as e:
            print(e)
            return

        if data["authenticated"]:
            yield response.follow(
                self.template_user_url % self.user_to_parse,
                # callback=self.parse_following,
                callback=self.user_page_parse,
                cb_kwargs={"username": self.user_to_parse},
            )

    def parse_following(self, response: HtmlResponse, username: str):
        user_id = self.fetch_user_id(response.text, username)
        url = "https://i.instagram.com/api/v1/friendships/%s/followers/?count=12&search_surface=follow_list_page"
        url = url % user_id
        yield response.follow(
            url,
            callback=self.parse_something,
            headers={
                "x-ig-app-id": "936619743392459",
            },
        )

    # TODO
    def parse_something(self, response: HtmlResponse):
        print("parse_something!")
        print(response.json())
        print()

    def user_page_parse(self, response: HtmlResponse, username: str):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            "id": user_id,
            "first": 12,
        }
        str_variables = self.make_str_variables(variables)
        url = self.post_getting_url % (self.post_query_hash, str_variables)
        print("TO POSTS!")
        print()
        yield response.follow(
            url,
            callback=self.post_parse,
            cb_kwargs={
                # глубокое копирование
                "variables": copy.deepcopy(variables),
                "username": username,
            },
        )

    def post_parse(self, response: HtmlResponse, variables: dict, username: str):
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print("Json decode error")
            print(e)
            return
        except Exception as e:
            print(e)
            return

        try:
            data = data["data"]["user"]["edge_owner_to_timeline_media"]
        except AttributeError as e:
            print("Error during getting edge_owner_to_timeline_media")
            print(e)
            return
        except KeyError as e:
            print("Error during getting edge_owner_to_timeline_media")
            print(e)
            return

        # getting with edges
        try:
            edges = data["edges"]
        except AttributeError as e:
            print("Error during getting page_info")
            print(e)
            return
        except KeyError as e:
            print("Error during getting page_info")
            print(e)
            return

        # work with edges
        for edge in edges:
            node = edge["node"]
            item = InstagramScraperItem()
            item["id"] = node["id"]
            item["user_id"] = variables["id"]
            item["username"] = username
            item["image_url"] = node["display_url"]
            item["metadata"] = node
            yield item

        # getting page_info
        try:
            page_info = data["page_info"]
        except AttributeError as e:
            print("Error during getting page_info")
            print(e)
            return
        except KeyError as e:
            print("Error during getting page_info")
            print(e)
            return

        # pagination
        if page_info["has_next_page"]:
            variables["after"] = page_info["end_cursor"]
            str_variables = self.make_str_variables(variables)
            url = self.post_getting_url % (self.post_query_hash, str_variables)
            yield response.follow(
                url,
                callback=self.post_parse,
                cb_kwargs={
                    # глубокое копирование
                    "variables": copy.deepcopy(variables),
                    "username": username,
                },
            )

    # get token for authorization
    def fetch_csrf_token(self, text):
        matched = re.search('"csrf_token":"\\w+"', text).group()
        return matched.split(":").pop().replace(r'"', "")

    # rollout_hash ; x_instagram_ajax
    def fetch_x_instagram_ajax(self, text):
        matched = re.search('"rollout_hash":"\\w+"', text).group()
        return matched.split(":").pop().replace(r'"', "")

    # get user_id for interesting user
    def fetch_user_id(self, text, username):
        matched = re.search('{"id":"\\d+","username":"%s"}' % username, text).group()
        return json.loads(matched).get("id")

    # encode variables dict
    def make_str_variables(self, variables):
        str_variables = quote(str(variables).replace(" ", "").replace("'", '"'))
        return str_variables
