import disnake
from disnake.ext import commands

from core import (
    DisnakeBot,
    Color,
    ButtonRoles,
    DevChannels,
    NoPerm,
    TagNotFound,
    Roles
)


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot: DisnakeBot = bot

    @commands.Cog.listener("on_button_click")
    async def button_click(self, interaction: disnake.MessageInteraction):
        match interaction.data.custom_id:
            case "tag_yes":
                embed: disnake.Embed = interaction.message.embeds[0]
                self.bot.database.update_guild_data(
                    "$set",
                    {f"tag_system.{embed.title}": {
                        "author": embed.footer.text,
                        "content": interaction.message.content
                    }}
                )

                await interaction.message.delete()
            case "tag_no":
                await interaction.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ButtonRoles(self.bot))
        print("Бот запущен")

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        channel = self.bot.get_channel(DevChannels.MESSAGE_LOGS)

        if message.author.bot:
            return
        if message.attachments:
            message.content += "картинка"
        if not message.content:
            message.content = "Нету"

        embed = disnake.Embed(
            title=message.author,
            description=f'**Удалил сообщение\nСообщение: \n```{message.content}```**',
            color=Color.GRAY
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_slash_command_error(self, interaction: disnake.CommandInteraction, error):
        error = getattr(error, "original", error)

        if isinstance(error, NoPerm):
            description = "У вас нету доступа"
        elif isinstance(error, TagNotFound):
            description = f"Тег {error} не найден!"
        else:
            description = "Ошибка!"

        await interaction.send(description)

    @commands.Cog.listener()
    async def on_thread_create(self, forum: disnake.Thread):
        role = forum.guild.get_role(Roles.HELP_ACTIVE)

        if forum.parent.id != DevChannels.FORUM:
            return
        if role in forum.owner.roles:
            return forum.edit(locked=True, archived=True)
            
        embed = disnake.Embed(
            title='Добро пожаловать',
            description='**Чтобы закрыть пост используйте: </close-post:1021401575106814013>**',
            color=Color.GRAY
        )

        msg = await forum.send(embed=embed)
        await forum.owner.add_roles(role, reason="Открыл запрос на помощь/баг")
        await msg.pin()

def setup(bot):
    bot.add_cog(Listeners(bot))
