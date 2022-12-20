import os
import dotenv
import hikari
import lightbulb
from selvbet_schedule import *
from absence import *

dotenv.load_dotenv()
bot = lightbulb.BotApp(
    os.environ["BOT_TOKEN"],
    intents=hikari.Intents.ALL,
    prefix="+",
    banner=None,
)

def limit_author_ids(*ids):
    @lightbulb.Check
    def inner(ctx: lightbulb.Context):
        if int(ctx.author.id) not in ids:
            raise lightbulb.CheckFailure("u are not allowed to run this cmd idiot")
        return True
    return inner

@bot.command
@lightbulb.command("ping", description="The bot's ping")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")

@bot.command
@lightbulb.option("target_class", description="specifies a target for the schedule")
@lightbulb.command("schedule", description="spits out selvbetjening schedule")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def schedule(ctx: lightbulb.Context) -> None:
    await ctx.respond("Fetching schedule...")
    get_schedule(str(ctx.options.target_class)) # fetches schedule and writes it to file
    with open("schedule.txt", "r") as f:
        contents = f.read()
        await ctx.respond(contents)

@bot.command
@lightbulb.option("present", description="number of classes present")
@lightbulb.option("absent", description="number of classes absent")
@lightbulb.option("skipamount", description="number of classes to skip")
@lightbulb.option("upcoming_classes_present", description="name :)")
@lightbulb.command("absence", description="spits out the absence % of janek :)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def absence(ctx: lightbulb.Context) -> None:
    # documentation can suck my dick.
    present = float(ctx.options.present)
    absent = float(ctx.options.absent)
    skipamount = float(ctx.options.skipamount)
    totalClasses = present + absent
    absencePercentage = (absent/totalClasses) * 100
    absencePercentage = round(absencePercentage, 2)
    present += float(ctx.options.upcoming_classes_present) 
    newTotalClasses = (totalClasses + skipamount)
    newAbsencePercentage = ((absent + skipamount)/newTotalClasses) * 100
    newAbsencePercentage = round(newAbsencePercentage, 2)

    await ctx.respond(f"Your current absence  is at {absencePercentage}%. Your new absence will be {newAbsencePercentage}%")

bot.run()
