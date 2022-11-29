import datetime

import disnake
from disnake.ext import commands

from core import DisnakeBot, Color, Roles


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot: DisnakeBot = bot

    @commands.slash_command()
    async def mod(self, interaction):
        ...

    @commands.has_any_role(Roles.MODER, Roles.HELPER)
    @mod.sub_command(name='mute', description='Выдать мут человеку.')
    async def mute(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member = commands.Param(
            description='Выберите пользователя'
        ),
        reason: str = commands.Param(
            description='Введите причину мута',
            default='Не указана'
        ),
        days: commands.Range[0, 28] = 0,
        hours: commands.Range[0, 23] = 0,
        minutes: commands.Range[0, 59] = 0,
    ):
        await interaction.response.defer(ephemeral=True)
        time = datetime.timedelta(days=days, hours=hours, minutes=minutes)
        embed = disnake.Embed(
            title='Мут пользователя',
            color=Color.GRAY
        )
        embed.set_author(
            name=member,
            icon_url=member.avatar.url
        )
        embed.set_footer(text=f'Причина: {reason}')

        await member.timeout(duration=time, reason=reason)
        await interaction.channel.send(embed=embed)
        await interaction.send("Готово")

    @commands.has_role(Roles.MODER)
    @mod.sub_command(name='ban', description='Выдать бан человеку.')
    async def ban(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member = commands.Param(
            description='Выберите пользователя'
        ),
        reason: str = commands.Param(
            description='Введите причину бана',
            default='Не указана'
        ),
    ):
        await interaction.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title='Блокировка пользователя',
            color=Color.GRAY
        )
        embed.set_author(
            name=member,
            icon_url=member.avatar.url
        )
        embed.set_footer(text=f'Причина: {reason}')

        await member.ban(reason=reason)
        await interaction.channel.send(embed=embed)
        await interaction.send("Готово")

    @commands.has_role(Roles.MODER)
    @mod.sub_command(name='kick', description='Кикнуть человека.')
    async def kick(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member = commands.Param(
            description='Выберите пользователя'
        ),
        reason: str = commands.Param(
            description='Введите причину кика',
            default='Не указана'
        ),
    ):
        await interaction.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title='Исключение пользователя',
            color=Color.GRAY
        )
        embed.set_author(
            name=member,
            icon_url=member.avatar.url
        )
        embed.set_footer(text=f'Причина: {reason}')

        await member.kick(reason=reason)
        await interaction.channel.send(embed=embed)
        await interaction.send("Готово")

    @commands.slash_command(name='solved', description='Закрыть вопрос')
    async def solved(self, interaction: disnake.GuildCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        if interaction.channel.owner.id != interaction.author.id or not interaction.author.guild_permissions.manage_messages:
            return await interaction.send("У вас нету доступа!")

        role = interaction.guild.get_role(Roles.HELP_ACTIVE)

        await interaction.channel.owner.remove_roles(role, reason='Закрыл запрос помощи')
        await interaction.channel.edit(locked=True, archived=True)
        await interaction.channel.send("Пост закрыт!")
        await interaction.send("Готово!")


def setup(bot):
    bot.add_cog(Moderation(bot))
