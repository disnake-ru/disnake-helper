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


class HelpButton(disnake.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot: DisnakeBot = bot

    async def send_helper(
        self,
        interaction: disnake.CommandInteraction,
        channel: disnake.TextChannel,
        type: str
    ):
        channel = self.bot.get_channel(LogChannel.BRANCH)
        embed = disnake.Embed(
            title=f'Новый вопрос по {type}',
            description=f'**Ветка: {channel.mention}\nАвтор: {interaction.author.mention}**',
            color=Color.GREEN
        )

        await channel.send("<@&983286061222473728>", embed=embed)

    async def help(
        self,
        interaction: disnake.MessageInteraction,
        type: str
    ):
        channel = await interaction.channel.create_thread(
            name=f'Помощь по {type} | {interaction.author}',
            type=disnake.ChannelType.public_thread
        )
        embed = disnake.Embed(
            title='Добро пожаловать',
            description=
f'''
**Если вам нужна помощь по {type}, будьте добрый выполнить следующие вещи: **
```
1) Описать вашу проблему/вопрос
2) Если это проблема, то отправить код и ошибку```
''',
            color=Color.GRAY
        )

        await self.send_helper(interaction, channel, type)
        await interaction.send(channel.mention, ephemeral=True)
        message = await channel.send(
            interaction.author.mention,
            embed=embed,
            view=CloseTread(self.bot)
        )
        await message.pin()

    @disnake.ui.button(label='Помощь disnake', style=disnake.ButtonStyle.grey, custom_id='disnake')
    async def disnake_n(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.defer(ephemeral=True)
        await self.help(interaction, "disnake")

    @disnake.ui.button(label='Помощь python', style=disnake.ButtonStyle.grey, custom_id='python')
    async def python(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.defer(ephemeral=True)
        await self.help(interaction, "python")


class CloseTread(disnake.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot: DisnakeBot = bot

    async def get_thread_author(self, channel: disnake.Thread):
        channel_history = channel.history(oldest_first=True, limit=1)
        history = await channel_history.flatten()
        member = history[0].mentions[0]
        return member.id

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        thread_author = await self.get_thread_author(interaction.channel)
        if interaction.user.id == thread_author or interaction.user.get_role(Roles.MODER) or interaction.user.get_role(Roles.HELPER):  # noqa: E501
            return True
        else:
            await interaction.send("Вам нельзя закрыть ветку", ephemeral=True)
            return False

    @disnake.ui.button(label='Закрыть ветку', style=disnake.ButtonStyle.red, custom_id='close')
    async def close(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        file = open(f"./logs/{interaction.author.id}.log", "w+", encoding='utf-8')
        channel = interaction.guild.get_channel(LogChannel.BRANCH)
        embed = disnake.Embed(
            title='Закрытие ветки',
            description='**История чата:**',
            color=Color.RED
        )
        message = []

        async for msg in interaction.channel.history(limit=200):
            if msg.author.bot:
                continue
            if msg.attachments:
                message.append(f"{msg.author}: фото\n")
            message.append(f"{msg.author}: {msg.clean_content}\n")
        for x in message:
            file.write(x)
        file.close()

        await channel.send(embed=embed, file=disnake.File(f"./logs/{interaction.author.id}.log"))
        await interaction.send("Ветка закрыта!")
        await interaction.channel.edit(archived=True, locked=True)
        os.remove(f"./utils/{interaction.author.id}.log")
