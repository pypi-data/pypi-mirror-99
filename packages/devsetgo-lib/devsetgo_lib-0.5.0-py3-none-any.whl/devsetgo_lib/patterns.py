# -*- coding: utf-8 -*-
import re
import logging


def pattern_between_two_char(
    text_string: str, left_characters: str, right_characters: str
) -> list:
    try:
        if left_characters.isprintable() is False:
            raise ValueError("The left character is not printable and cannot be used.")

        if right_characters.isprintable() is False:
            raise ValueError("The right character is not printable and cannot be used.")

        esc_text = re.escape(text_string)
        esc_left_char = re.escape(left_characters)
        esc_right_char = re.escape(right_characters)

        pattern = f"{esc_left_char}(.+?){esc_right_char}+?"

        pattern_list = re.findall(pattern, esc_text)
        results: dict = {
            "found": pattern_list,
            "matched_found": len(pattern_list),
            "pattern_parameters": {
                "left_character": esc_left_char,
                "right_character": esc_right_char,
                "regex_pattern": pattern,
                "text_string": esc_text,
            },
        }

        return results

    except ValueError as e:
        # capture exception and return results
        results: dict = {
            "Error": str(e),
            "matched_found": 0,
            "pattern_parameters": {
                "left_character": left_characters,
                "right_character": right_characters,
                "regex_pattern": None,
                "text_string": text_string,
            },
        }
        # logging of regex error
        logging.critical(results)
        return results


"""
leaving for future use

# def pattern_between(
#     text_string: str, left_character: str, right_character: str, split_character: str
# ) -> dict:
#     lr_list = [left_character, right_character]

#     try:
#         # escape input strings if necessary
#         esc_text = re.escape(text_string)
#         esc_left_char = re.escape(left_character)
#         esc_right_char = re.escape(right_character)
#         esc_split_char = re.escape(split_character)
#         # print(esc_split_char)

#         # regex pattern to find values between
#         pattern = f".*{esc_left_char}(.*){esc_right_char}.*"
#         # split string by a character
#         text_items = esc_text.split(esc_split_char)
#         if split_character in lr_list:
#             raise Exception

#         # list to hold matched patterns
#         pattern_list: list = []

#         # loop through list of items and check for pattern
#         for i in text_items:
#             item = re.match(pattern, i)

#             # if pattern matched, then add to a list to be returned
#             if item is not None:
#                 pattern_list.append(item)

#         results: dict = {
#             "found": pattern_list,
#             "matched_found": len(pattern_list),
#             "pattern_parameters": {
#                 "left_character": esc_left_char,
#                 "right_character": esc_right_char,
#                 "split_character": esc_split_char,
#                 "regex_pattern": pattern,
#                 "text_string": esc_text,
#             },
#         }
#         return results
#     except re.error as e:
#         # capture exception and return results
#         results: dict = {
#             "Error": e,
#             "matched_found": 0,
#             "pattern_parameters": {
#                 "left_character": esc_left_char,
#                 "right_character": esc_right_char,
#                 "split_character": esc_split_char,
#                 "regex_pattern": pattern,
#                 "text_string": esc_text,
#             },
#         }
#         # logging of regex error
#         logging.critical(results)
#         # return of results
#         return results
#     except Exception as e:
#         # capture exception and return results
#         e = f"the split character '{split_character}' is the same as the left
#         '{left_character}' or right character '{right_character}'.
#         Making this an invalid combination."
#         results: dict = {
#             "Error": e,
#             "matched_found": 0,
#             "pattern_parameters": {
#                 "left_character": esc_left_char,
#                 "right_character": esc_right_char,
#                 "split_character": esc_split_char,
#                 "regex_pattern": pattern,
#                 "text_string": esc_text,
#             },
#         }
#         # logging of regex error
#         logging.critical(results)
#         # return of results
#         return results
"""
