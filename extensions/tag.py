import disnake
from disnake.ext import commands

from core import DisnakeBot, TagCreate, TagNotFound, NoPerm, HelpButton


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot: DisnakeBot = bot

    async def edit_delete_tag(interaction: disnake.CommandInteraction, user_input: str):
        collection = interaction.bot.database.get_guild_data()
        database = collection.find_one({"_id": "settings"})["tag_system"]
        tags = []

        for tag in database:
            if interaction.author.guild_permissions.administrator:
                tags.append(tag)
            else:
                if database[str(tag)]['author'] == interaction.author.id:
                    tags.append(tag)

        return [tag for tag in tags if user_input.lower() in tag]

    @commands.slash_command()
    async def tag(self, interaction):
        ...

    @tag.sub_command(name='create', description='Создать тег.')
    async def create(self, interaction: disnake.CommandInteraction):
        await interaction.response.send_modal(TagCreate(self.bot))

    @tag.sub_command(name='delete', description='Удалить тег.')
    async def delete(
        self,
        interaction: disnake.CommandInteraction,
        tag: str = commands.Param(
            description='Введите имя тега',
            autocomplete=edit_delete_tag
        )
    ):
        await interaction.response.defer()
        tag = self.bot.database.get_tag(tag)

        if not tag:
            raise TagNotFound(tag)
        if tag['author'] != interaction.author.id and not interaction.author.guild_permissions.administrator:  # noqa: E501
            raise NoPerm

        self.bot.database.update_guild_data(
            "$unset",
            {f"tag_system.{tag}": ""}
        )

        await interaction.send("Вы успешно удалили тег")

    @tag.sub_command(name='open', description='Открыть тег.')
    async def open(
        self,
        interaction: disnake.CommandInteraction,
        tag: str = commands.Param(
            description='Введите имя тега',
        )
    ):
        await interaction.response.defer()
        tag = self.bot.database.get_tag(tag)

        if not tag:
            raise TagNotFound(tag)

        await interaction.send(content=tag['content'])

    @commands.slash_command(name='asd')
    async def asd(self, interaction: disnake.CommandInteraction):
        await interaction.response.defer(ephemeral=True)
        message = await interaction.channel.fetch_message(1008434012106260490)
        await message.edit(view=HelpButton(self.bot))

    @open.autocomplete("tag")
    async def tag_open(self, interaction: disnake.CommandInteraction, string: str):
        collection = self.bot.get_guild_data()
        data = collection.find_one({"_id": "settings"})["tag_system"]
        message = []

        for x in data:
            message.append(x)
        return [tag for tag in message if string.lower() in tag]


def setup(bot):
    bot.add_cog(Tags(bot))
