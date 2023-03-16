import disnake
from disnake.ext import commands
from loguru import logger

from core import (
    DisnakeBot,
    Color,
    DevChannels,
    NoPerm,
    TagNotFound,
    Roles
)


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot: DisnakeBot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.success(f"Бот запущен успешно с аккаунта {self.bot}")

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        channel = self.bot.get_channel(DevChannels.MESSAGE_LOGS)

        if message.author.bot:
            return
        if message.attachments:
            message.content += "🖼 картинка"
        if not message.content:
            message.content = "*🕳 Отсутствует*"

        embed = disnake.Embed(
            title=message.author,
            description=f'**Удалил сообщение из {message.channel.mention}\nСообщение: \n```{message.content}```**',
            color=Color.GRAY
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_slash_command_error(self, interaction: disnake.CommandInteraction, error: Exception):
        error = getattr(error, "original", error)

        if isinstance(error, NoPerm):
            description = "✋ У вас нет доступа"
        elif isinstance(error, TagNotFound):
            description = f"👀 Тег {error} не найден!"
        else:
            description = "⚠ Ошибка!"

        await interaction.send(description, ephemeral=True)

    @commands.Cog.listener("on_thread_create")
    async def thread_create_detect(self, forum: disnake.Thread):
        role = forum.guild.get_role(Roles.HELP_ACTIVE)

        if forum.parent.id != DevChannels.FORUM:
            return
        if role in forum.owner.roles:
            return forum.edit(locked=True, archived=True)

        embed = disnake.Embed(
            title='Добро пожаловать',
            description='**Воспользуйтесь </solved:1047221256354812026> для закрытия поста, если вопрос решён.**',
            color=Color.GRAY
        )

        msg = await forum.send(embed=embed)
        await forum.owner.add_roles(role, reason="Открыл запрос на помощь/баг")
        await msg.pin()


def setup(bot):
    bot.add_cog(Listeners(bot))
