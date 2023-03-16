import disnake
from disnake.ext import commands

from core import DisnakeBot, Color, SELECT_ROLES_LIST


class ComponentsListeners(commands.Cog):
    def __init__(self, bot):
        self.bot: DisnakeBot = bot

    @commands.Cog.listener("on_button_click")
    async def button_click(self, interaction: disnake.MessageInteraction):
        match interaction.data.custom_id:
            case "tag_yes":
                embed: disnake.Embed = interaction.message.embeds[0]
                self.bot.database.update_guild_data(
                    "$set",
                    {
                        f"tag_system.{embed.title}":
                            {
                                "author": embed.footer.text,
                                "content": interaction.message.content
                            }
                    }
                )

                await interaction.message.delete()
            case "tag_no":
                await interaction.message.delete()

    @commands.Cog.listener("on_dropdown")
    async def select_delect(self, interaction: disnake.MessageInteraction):
        match interaction.data.custom_id:
            case "server_info":
                match interaction.values[0]:
                    case "staff":
                        embed = disnake.Embed(
                            title='Список стаффа сервера disnake[ru]',
                            description='**<@175856311827693568> `-` `Владелец, Модератор`\n<@495905651365642250> `-` `Владелец, Модератор`\n<@450229150217797633> `-` `Модератор`\n<@301295716066787332> `-` `Разработчик disnake`**',
                            color=Color.GRAY
                        )
                        embed.set_thumbnail(url=interaction.guild.icon.url)
                    case "server":
                        embed = disnake.Embed(
                            description='**coming soon**',
                            color=Color.GRAY
                        )
                    case "roles":
                        embed = disnake.Embed(
                            title='Список ролей сервера',
                            description=f'**<@&983325422471229521> `-` `Разработчики disnake`\n<@&983133009144324250> `-` `Модераторы`\n<@&983286061222473728> `-` `Хелперы`\n<@&1064141360917119047> `-` `Человек который много помогает и может стать хелпером`\n<@&1004072426486906992> `-` `Бустеры`\n<@&991386954732146749> `-` `Создатели видеоконтента`\n<@&1016372025062858833> `-` `Благодарность за помощь серверу`\n<@&984114185493426226> `-` `ЧС помощи`\n\n<@&991387100639404172> `-` `Уведомления о новых роликах`\n<@&983441082039820329> `-` `Уведомления о обновлениях disnake`\n<@&983441129276063834> `-` `Уведомления о новостях сервера`\n<@&1008439902280630272> `-` `Уведомления о голосованиях disnake`**',
                            color=Color.GRAY
                        )
                if interaction.values[0] == "roles":
                    await interaction.send(
                        embed=embed,
                        components=[
                            disnake.ui.StringSelect(
                                custom_id="get_role",
                                placeholder='Нажми сюда, чтобы получить роль',
                                options=[
                                    disnake.SelectOption(label=data['label'], value=data['value'])
                                    for data in SELECT_ROLES_LIST
                                ]
                            )
                        ],
                        ephemeral=True
                    )
                else:
                    await interaction.send(embed=embed, ephemeral=True)
            case "get_role":
                role = interaction.guild.get_role(int(interaction.values[0]))

                if role in interaction.author.roles:
                    await interaction.author.remove_roles(role)
                else:
                    await interaction.author.add_roles(role)

                await interaction.send("✅", ephemeral=True)
            case "urls":
                embed = disnake.Embed(
                    title='Ссылки:',
                    description='''
Disnake GitHub: https://github.com/DisnakeDev/disnake

Disnake Docs: https://disnake.readthedocs.io/en/stable

Disnake PyPI: https://pypi.org/project/disnake

Disnake guide: https://guide.disnake.dev/

Disnake[RU] Github: https://github.com/disnake-ru

Disnake[RU] guilde: https://ru.guide.disnake.dev
''',
                    color=Color.GRAY
                )
                await interaction.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ComponentsListeners(bot))
