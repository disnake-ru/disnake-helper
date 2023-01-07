import datetime

import disnake
from disnake.ext import commands

from core import DisnakeBot, Color, Roles, DevChannels


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot: DisnakeBot = bot

    @commands.slash_command(
        name=disnake.Localized("mod", key="MOD")
    )
    async def mod(self, interaction):
        ...

    @commands.has_any_role(Roles.MODER, Roles.HELPER)
    @mod.sub_command(
        name=disnake.Localized("mute", key="MUTE"),
        description=disnake.Localized("Mute the calmbreaker!", key="MUTE_DESCR")
    )
    async def mute(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("member", key="TARGET_MEMBER"),
            description=disnake.Localized(
                "The calmbreaker which his fate have decided by the Council",
                key="MUTE_MEMBER_DESCR"
            )
        ),
        reason: str = commands.Param(
            name=disnake.Localized("reason", key="REASON"),
            description=disnake.Localized("Provide the reason", key="WHY"),
            default='Not provided | Не указана'
        ),
        # days: commands.Range[0, 28] = 0,
        # hours: commands.Range[0, 23] = 0,
        # minutes: commands.Range[0, 59] = 0,
        days: int = commands.Param(
            name=disnake.Localized("days", key="MUTE_DAYS"),
            description=disnake.Localized("Amount of days of punishment", key="MUTE_DAYS_DESCR"),
            max_value=28,
            min_value=0,
            default=0
        ),
        hours: int = commands.Param(
            name=disnake.Localized("hours", key="MUTE_HOURS"),
            description=disnake.Localized("Amount of hours of punishment", key="MUTE_HOURS_DESCR"),
            max_value=24,
            min_value=0,
            default=0
        ),
        minutes: int = commands.Param(
            name=disnake.Localized("minuets", key="MUTE_MINUTES"),
            description=disnake.Localized("Amount of minutes of punishment", key="MUTE_MINUTES_DESCR"),
            max_value=60,
            min_value=0,
            default=0
        ),
    ):
        await interaction.response.defer(ephemeral=True)
        time = datetime.timedelta(days=days, hours=hours, minutes=minutes)
        embed = disnake.Embed(
            title='Мьют пользователя',
            color=Color.GRAY
        )
        embed.set_author(
            name=member,
            icon_url=member.avatar.url
        )
        embed.add_field(
            name="Причина:",
            value=reason if reason != "Not provided | Не указана" else "*История умалчивает...*"
        )

        await member.timeout(duration=time, reason=reason)
        await interaction.channel.send(embed=embed)
        await interaction.send("👍 Готово")

    @commands.has_role(Roles.MODER)
    @mod.sub_command(
        name=disnake.Localized("gulag", key="GULAG"),
        description=disnake.Localized("Send the unwanted person to Siberia...", key="GULAG_DESCR")
    )
    async def ban(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("villain", key="GULAG_TARGET"),
            description=disnake.Localized("Who deserved to be sent to GULAG?", key="GULAG_TARGET_DESCR")
        ),
        reason: str = commands.Param(
            name=disnake.Localized("reason", key="REASON"),
            description=disnake.Localized("Announce the reason!", key="GULAG_REASON_DESCR"),
            default="Not provided | Не указана"
        ),
    ):
        await interaction.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title='Ссылка пользователя в ГУЛАГ',
            description=f"*Пользователь {member.mention} предстал перед **Советским Союзом** по побвинению в покушении на **Сталина**...*",
            color=Color.GRAY
        )
        embed.set_author(
            name=member,
            icon_url=member.avatar.url
        )
        embed.add_field(
            name=f'Причина ссылки:',
            value=reason if reason != "Not provided | Не указана" else "*История умалчивает...*"
        )

        await member.ban(reason=reason)
        await interaction.channel.send(embed=embed)
        await interaction.send("👍 Готово")

    @commands.has_role(Roles.MODER)
    @mod.sub_command(
        name=disnake.Localized("kick", key="KICK"),
        description=disnake.Localized("Kick member", key="KICK_DESCR")
    )
    async def kick(
        self,
        interaction: disnake.GuildCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("member", key="TARGET_MEMBER"),
            description=disnake.Localized("Provide the reason", key="WHY")
        ),
        reason: str = commands.Param(
            name=disnake.Localized("reason", key="REASON"),
            description=disnake.Localized("Provide the reason", key="WHY"),
            default="Not provided | Не указана"
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
        embed.add_field(
            name='Причина:',
            value=reason if reason != "Not provided | Не указана" else "*История умалчивает...*"
        )

        await member.kick(reason=reason)
        await interaction.channel.send(embed=embed)
        await interaction.send("👍 Готово")

    @commands.slash_command(
        name=disnake.Localized("solved", key="POST_SOLVED"),
        description=disnake.Localized(
            "Mark this post as solved and lock it",
            key="POST_SOLVED_DESCR"
        )
    )
    async def solved(self, interaction: disnake.GuildCommandInteraction):
        if interaction.channel.parent_id is None:  # != DevChannels.FORUM:
            return await interaction.send("❌ Нельзя закрыть не пост!", ephemeral=True)
        
        await interaction.response.defer(ephemeral=True)

        if interaction.channel.owner.id != interaction.author.id and not interaction.author.guild_permissions.manage_messages:
            return await interaction.send("✋ У вас нет доступа к закрытию этого поста!")

        role = interaction.guild.get_role(Roles.HELP_ACTIVE)

        await interaction.channel.owner.remove_roles(role, reason='Закрыл запрос помощи')
        await interaction.channel.edit(locked=True, archived=True)
        await interaction.channel.send("Пост закрыт!")
        await interaction.send("Готово!")

def setup(bot):
    bot.add_cog(Moderation(bot))
