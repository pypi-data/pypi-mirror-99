"""
Market Shenanigans
"""

import logging
import requests

# Cog Stuff
from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Color


logger = logging.getLogger(__name__)


class PriceCheck(commands.Cog):
    """
    price checks on Jita and Amarr markets
    """

    @commands.command(pass_context=True)
    async def price(self, ctx):
        """
        Check an item price on Jita and Amarr market
        :param ctx:
        :return:
        """

        has_thumbnail = False

        await ctx.trigger_typing()

        item_name = ctx.message.content[7:]

        embed = Embed(
            title="Price Lookup (Jita and Amarr) for {item_name}".format(
                item_name=item_name
            ),
            color=Color.green(),
        )

        embed.add_field(
            name="Jita Market",
            value="Prices for {item_name} on the Jita Market.".format(
                item_name=item_name
            ),
            inline=False,
        )

        # Jita Market
        jita_market = requests.post(
            "https://evepraisal.com/appraisal/structured.json",
            json={"market_name": "jita", "items": [{"name": item_name}]},
        )

        if jita_market.status_code == 200:
            jita_json = jita_market.json()

            has_thumbnail = True
            embed.set_thumbnail(
                url="https://images.evetech.net/types/{type_id}/icon?size=64".format(
                    type_id=jita_json["appraisal"]["items"][0]["typeID"]
                )
            )

            # sell order price
            jita_market_sell_order_price = (
                f'{jita_json["appraisal"]["items"][0]["prices"]["sell"]["min"]:,} ISK'
            )

            if jita_json["appraisal"]["items"][0]["prices"]["sell"]["order_count"] == 0:
                jita_market_sell_order_price = "No sell orders found"

            embed.add_field(
                name="Sell Order Price",
                value=jita_market_sell_order_price,
                inline=True,
            )

            # buy order price
            jita_market_buy_order_price = (
                f'{jita_json["appraisal"]["items"][0]["prices"]["buy"]["max"]:,} ISK'
            )

            if jita_json["appraisal"]["items"][0]["prices"]["buy"]["order_count"] == 0:
                jita_market_buy_order_price = "No buy orders found"

            embed.add_field(
                name="Buy Order Price",
                value=jita_market_buy_order_price,
                inline=True,
            )
        else:
            embed.add_field(
                name="API Error",
                value="Couldn't not fetch the price for the Jita market.",
                inline=False,
            )

        embed.add_field(
            name="Amarr Market",
            value="Prices for {item_name} on the Amarr Market.".format(
                item_name=item_name
            ),
            inline=False,
        )

        # Amarr Market
        amarr_market = requests.post(
            "https://evepraisal.com/appraisal/structured.json",
            json={"market_name": "amarr", "items": [{"name": item_name}]},
        )

        if amarr_market.status_code == 200:
            amarr_json = amarr_market.json()

            if has_thumbnail is False:
                embed.set_thumbnail(
                    url=(
                        "https://images.evetech.net/types/{type_id}/icon?size=64"
                    ).format(type_id=amarr_json["appraisal"]["items"][0]["typeID"])
                )

            # sell order price
            amarr_market_sell_order_price = (
                f'{amarr_json["appraisal"]["items"][0]["prices"]["sell"]["min"]:,} ISK'
            )

            if (
                amarr_json["appraisal"]["items"][0]["prices"]["sell"]["order_count"]
                == 0
            ):
                amarr_market_sell_order_price = "No sell orders found"

            embed.add_field(
                name="Sell Order Price",
                value=amarr_market_sell_order_price,
                inline=True,
            )

            # buy order price
            amarr_market_buy_order_price = (
                f'{amarr_json["appraisal"]["items"][0]["prices"]["buy"]["max"]:,} ISK'
            )

            if amarr_json["appraisal"]["items"][0]["prices"]["buy"]["order_count"] == 0:
                amarr_market_buy_order_price = "No buy orders found"

            embed.add_field(
                name="Buy Order Price",
                value=amarr_market_buy_order_price,
                inline=True,
            )
        else:
            embed.add_field(
                name="API Error",
                value="Couldn't not fetch the price for the Amarr market.",
                inline=False,
            )

        return await ctx.send(embed=embed)


def setup(bot):
    """
    add the cogg
    :param bot:
    :return:
    """
    bot.add_cog(PriceCheck(bot))
