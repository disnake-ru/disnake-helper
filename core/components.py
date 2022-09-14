import os

import disnake

from . import DisnakeBot, LogChannel, Color, Roles


class TagCreate(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot: DisnakeBot = bot
        components = [
            disnake.ui.TextInput(
                label="Имя тега",
                custom_id="name",
                style=disnake.TextInputStyle.short,
                max_length=25,
            ),
            disnake.ui.TextInput(
                label="Содержание тега",
                custom_id="description",
                style=disnake.TextInputStyle.paragraph,
                min_length=5,
            )
        ]

        super().__init__(
            title="Создать Тег",
            custom_id="create_tag",
            components=components
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        channel = interaction.guild.get_channel(LogChannel.MOD_LOG)
        modal = interaction.text_values
        tag = self.bot.database.check_tag(modal['name'])

        if not tag:
            return await interaction.response.send_message('Имя уже занято', ephemeral=True)

        embed = disnake.Embed(
            title=modal["name"],
            color=Color.GRAY
        )
        embed.set_footer(
            icon_url=interaction.author.avatar.url,
            text=interaction.author.id
        )

        await channel.send(
            content=modal["description"],
            embed=embed,
            components=[
                disnake.ui.Button(
                    label='Принять',
                    custom_id='tag_yes',
                    style=disnake.ButtonStyle.green
                ),
                disnake.ui.Button(
                    label='Отклонить',
                    custom_id='tag_no',
                    style=disnake.ButtonStyle.red
                )
            ]
        )
        await interaction.response.send_message('Ваш тег отправлен на проверку', ephemeral=True)


class ButtonRoles(disnake.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot: DisnakeBot = bot

    async def interaction_click(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        role = interaction.guild.get_role(int(button.custom_id))

        if role in interaction.author.roles:
            text = "**Вы успешно сняли роль**"
            await interaction.author.remove_roles(role)
        else:
            text = "**Вы успешно добавили роль**"
            await interaction.author.add_roles(role)

        await interaction.response.send_message(text, ephemeral=True)

    @disnake.ui.button(label='Обновления', custom_id='983441082039820329')
    async def update(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.interaction_click(button, interaction)

    @disnake.ui.button(label='Новости', custom_id='983441129276063834')
    async def news(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.interaction_click(button, interaction)

    @disnake.ui.button(label='Гайды', custom_id='991387100639404172')
    async def guilds(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.interaction_click(button, interaction)

    @disnake.ui.button(label='Голосования', custom_id='1008439902280630272')
    async def pull(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.interaction_click(button, interaction)