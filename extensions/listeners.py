import disnake
from disnake.ext import commands, invitetracker

from core import (
    DisnakeBot,
    Color,
    ButtonRoles,
    LogChannel,
    HelpButton,
    CloseTread,
    NoPerm,
    TagNotFound
)


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot: DisnakeBot = bot
        self.invite = invitetracker.InviteLogger(bot)

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
        self.bot.add_view(HelpButton(self.bot))
        self.bot.add_view(CloseTread(self.bot))
        print("Бот запущен")

    @commands.Cog.listener("on_member_join")
    async def member_join(self, member: disnake.Member):
        invite: disnake.Invite = await self.invite.get_invite(member)
        channel = self.bot.get_channel(LogChannel.ON_MEMBER_JOIN)
        embed = disnake.Embed(
            description=f'**Создан: <t:{int(member.joined_at.timestamp())}:F>)\nПригласил: {invite.inviter.mention}**',  # noqa: E501
            color=Color.GRAY
        )
        embed.set_author(name=member, icon_url=member.avatar.url)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        channel = self.bot.get_channel(LogChannel.MESSAGE_LOGS)

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
    async def on_message(self, message: disnake.Message):
        if message.channel.id == 1008412847488913518:
            await message.delete()

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


def setup(bot):
    bot.add_cog(Listeners(bot))
