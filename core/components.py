import disnake

from . import DisnakeBot, DevChannels, Color


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
        channel = interaction.guild.get_channel(DevChannels.MOD_LOG)
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