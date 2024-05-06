from discord.ext import commands


def has_any_role(*items):
    return commands.check_any(
        commands.is_owner(),
        commands.has_permissions(administrator=True),
        commands.has_any_role(*items),
    )


def is_admin():
    return has_any_role(1234852012420497500)


def is_manager():
    return has_any_role(1234852096751177729)


def is_moderator():
    return has_any_role(1234852096751177729, 1234852158659231744)


def is_trial_moderator():
    return has_any_role(1234852096751177729, 1234852158659231744, 1234852421260279839)


def is_server_booster():
    return has_any_role("Server Booster")


def has_min_level(level):
    async def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage()

        query = {"_id": ctx.author.id}
        entry = await ctx.bot.mongo.db.member.find_one(
            query, {"$setOnInsert": query}, upsert=True, return_document=True
        )

        if entry.get("level", 0) >= level:
            return True

        raise commands.CheckFailure(
            f"You must be at least **Level {level}** to use this command."
        )

    return commands.check(predicate)
