import discord
from discord.ext import commands
import errors
import emoji as emoji_module

class ErrorGenerator():
    __author__ = "Dreammaker#1871"
    __version__ = "0.0.1"

    __slots__ = [
        'title',
        'description',
        'color',
        'code',
        'emoji',
        'footer',
        'lang'
    ]

    def __init__(
        self,
        title: str=None,
        description: str=None,
        emoji: str=None,
        color: int=None,
        code: int=None,
        footer: str=None,
        lang: str=None
    ):
        self.title = title
        self.description = description
        self.emoji = emoji
        self.color = color
        self.code = code
        self.footer = footer
        self.lang = lang

        if description is None:
            raise errors.MissingArgument("Description is a required argument that is missing.")
        else:
            if not isinstance(description, str):
                raise errors.BadObjectType("Description object must be string.")

        if title is None:
            pass
        else:
            if not isinstance(title, str):
                raise errors.BadObjectType("Title object must be string.")

        if color is None:
            pass
        else:
            if not isinstance(color, int):
                raise errors.BadObjectType("Color object must be integer.")

        if emoji is None:
            pass
        else:
            if not isinstance(emoji, str):
                raise errors.BadObjectType("Emoji object must be string.")
            else:
                if ":" not in emoji_module.demojize(emoji):
                    raise errors.MissingEmoji("Emoji object has't any emoji.")

        if code is None:
            pass
        else:
            if not isinstance(code, int):
                raise errors.BadObjectType("Code object must be integer.")

        if footer is None:
            pass
        else:
            if not isinstance(footer, str):
                raise errors.BadObjectType("Footer object must be string.")
    
        if lang is None:
            raise errors.MissingArgument("Language is a required argument that is missing.")
        else:
            if not isinstance(lang, str):
                raise errors.BadObjectType("Language object must be string.")

    async def send_error(self, ctx):
        embed = discord.Embed()
        
        if self.emoji is None:
            self.emoji = "❌"

        if self.lang == "ru":
            if self.code is None:
                self.code = ""
            else:
                self.code = f"Код ошибки: {self.code}"

            if self.title is None:
                embed.title = self.emoji + " " + "Ошибка!"
            else:
                embed.title = self.emoji + " " + self.title

        elif self.lang == "en":
            if self.code is None:
                self.code = ""
            else:
                self.code = f"Code of error: {self.code}"

            if self.title is None:
                embed.title = self.emoji + " " + "Error!"
            else:
                embed.title = self.emoji + " " + self.title

        else:
            raise errors.BadLanguage(f'Language "{self.language}" is not found.')

        embed.description = self.description + "\n\n" + self.code

        if self.color is None:
            embed.color = 0xFF0000
        else:
            embed.color = self.color

        if self.footer is None:
            pass
        else:
            embed.set_footer(text=self.footer)

        return await ctx.send(embed = embed)

    async def generate_error(self):
        embed = discord.Embed()

        if self.emoji is None:
            self.emoji = "❌"

        if self.lang == "ru":
            if self.code is None:
                self.code = ""
            else:
                self.code = f"Код ошибки: {self.code}"

            if self.title is None:
                embed.title = self.emoji + " " + "Ошибка!"
            else:
                embed.title = self.emoji + " " + self.title

        elif self.lang == "en":
            if self.code is None:
                self.code = ""
            else:
                self.code = f"Code of error: {self.code}"

            if self.title is None:
                embed.title = self.emoji + " " + "Error!"
            else:
                embed.title = self.emoji + " " + self.title

        else:
            raise errors.BadLanguage(f'Language "{self.language}" is not found.')

        embed.description = self.description + "\n\n" + self.code

        if self.color is None:
            embed.color = 0xFF0000
        else:
            embed.color = self.color

        if self.footer is None:
            pass
        else:
            embed.set_footer(text=self.footer)

        return embed