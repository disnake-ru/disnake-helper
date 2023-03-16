import disnake
from disnake.ext import commands

from core import DisnakeBot, TagCreate, TagNotFound, NoPerm


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

    @commands.slash_command(
        name=disnake.Localized("tag", key="TAG")
    )
    async def tag(self, interaction: disnake.GuildCommandInteraction):
        ...

    @tag.sub_command(
        name=disnake.Localized("create", key="TAG_CREATE"),
        description=disnake.Localized("Create tag", key="TAG_CREATE_DESCR")
    )
    async def create(self, interaction: disnake.GuildCommandInteraction):
        await interaction.response.send_modal(TagCreate(self.bot))

    @tag.sub_command(
        name=disnake.Localized("delete", key="TAG_DELETE"),
        description=disnake.Localized("Remove the tag from tag database", key="TAG_DELETE_DESCR")
    )
    async def delete(
        self,
        interaction: disnake.GuildCommandInteraction,
        tag: str = commands.Param(
            name=disnake.Localized("tagname", key="TAG_DELETE_TAGNAME_NAME"),
            description=disnake.Localized("Tag's name which require to remove", key="TAG_DELETE_TAGNAME_DESCR"),
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

    async def tag_open_autocomp(interaction: disnake.CommandInteraction, string: str):
        collection = interaction.bot.database.get_guild_data()
        data = collection.find_one({"_id": "settings"})["tag_system"]
        message = []

        for x in data:
            message.append(x)
        return [tag for tag in message if string.lower() in tag]

    @tag.sub_command(
        name=disnake.Localized("open", key="TAG_READ"),
        description=disnake.Localized("Open a tag", key="TAG_READ_DESCR")
    )
    async def open(
        self,
        interaction: disnake.GuildCommandInteraction,
        tag_name: str = commands.Param(
            name=disnake.Localized("taganme", key="TAG_READ_TAGNAME_NAME"),
            description=disnake.Localized("Tag's name which require to open", key="TAG_READ_TAGNAME_DESCR"),
            autocomplete=tag_open_autocomp
        )
    ):
        await interaction.response.defer()
        tag = self.bot.database.get_tag(tag_name)

        if not tag:
            raise TagNotFound(tag_name)

        await interaction.send(content=tag['content'])


def setup(bot):
    bot.add_cog(Tags(bot))
