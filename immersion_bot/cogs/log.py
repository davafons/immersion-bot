import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional

import discord
import helpers
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from sql import Set_Goal, Store, MediaType

#############################################################

load_dotenv()

_DB_NAME = os.environ["PROD_DB_PATH"]

guildid = int(os.environ["GUILD_ID"])
channelid = int(os.environ["CHANNEL_ID"])

log = logging.getLogger(__name__)

#############################################################


class Log(commands.Cog):
    log_group = app_commands.Group(name="log", description="Log commands")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.myguild = self.bot.get_guild(guildid)

    @log_group.command(name="anime", description="Registra un anime")
    @app_commands.describe(episodios="Número de episodios vistos")
    @app_commands.describe(
        tiempo="""Tiempo, si no se especifica el bot asume 20 min por episodio. Formatos aceptados: 01:20, 20, 20min, 1h"""
    )
    @app_commands.describe(nombre="""Nombre del anime""")
    @app_commands.describe(comentario="""Comentario extra a registrar""")
    @app_commands.describe(
        backlog="""Registra en un día anterior. Formato aceptado: [yyyy-mm-dd]. Ejemplo: 2024-02-01"""
    )
    async def log_anime(
        self,
        interaction: discord.Interaction,
        episodios: int,
        tiempo: Optional[str],
        nombre: str,
        comentario: Optional[str],
        backlog: Optional[str],
    ):
        await interaction.response.defer()

        if episodios > 20:
            return await interaction.edit_original_response(
                content="No se pueden registrar más de 20 episodios de una vez."
            )
        if episodios < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        time_spent_min = 20 * episodios
        if tiempo:
            time_spent_min = helpers.elapsed_time_to_mins(tiempo)
        if time_spent_min < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        return await self.log(
            interaction,
            MediaType.ANIME.value,
            episodios,
            time_spent_min,
            nombre,
            comentario,
            backlog,
        )

    @log_group.command(name="manga", description="Registra un manga")
    @app_commands.describe(paginas="Número de páginas leídas")
    @app_commands.describe(
        tiempo="""Tiempo estimado que ha estado leyendo. Formatos aceptados: 01:20, 20, 20min, 1h"""
    )
    @app_commands.describe(nombre="""Nombre del manga""")
    @app_commands.describe(comentario="""Comentario extra a registrar""")
    @app_commands.describe(
        backlog="""Registra en un día anterior. Formato aceptado: [yyyy-mm-dd]. Ejemplo: 2024-02-01"""
    )
    async def log_manga(
        self,
        interaction: discord.Interaction,
        paginas: int,
        tiempo: str,
        nombre: str,
        comentario: Optional[str],
        backlog: Optional[str],
    ):
        await interaction.response.defer()

        if paginas > 3000:
            return await interaction.edit_original_response(
                content="No se pueden registrar más de 3000 páginas de una vez."
            )
        if paginas < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        time_spent_min = helpers.elapsed_time_to_mins(tiempo)
        if time_spent_min < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        return await self.log(
            interaction,
            MediaType.MANGA.value,
            paginas,
            time_spent_min,
            nombre,
            comentario,
            backlog,
        )

    @log_group.command(name="vn", description="Registra progreso en una VN")
    @app_commands.describe(caracteres="Número de caracteres leídos")
    @app_commands.describe(
        tiempo="""Tiempo estimado que ha estado leyendo. Formatos aceptados: 01:20, 20, 20min, 1h"""
    )
    @app_commands.describe(nombre="""Nombre de la VN""")
    @app_commands.describe(comentario="""Comentario extra a registrar""")
    @app_commands.describe(
        backlog="""Registra en un día anterior. Formato aceptado: [yyyy-mm-dd]. Ejemplo: 2024-02-01"""
    )
    async def log_vn(
        self,
        interaction: discord.Interaction,
        caracteres: int,
        tiempo: str,
        nombre: str,
        comentario: Optional[str],
        backlog: Optional[str],
    ):
        await interaction.response.defer()

        if caracteres > 200000:
            return await interaction.edit_original_response(
                content="No se pueden registrar más de 200000 caracteres de una vez."
            )
        if caracteres < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        time_spent_min = helpers.elapsed_time_to_mins(tiempo)
        if time_spent_min < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        return await self.log(
            interaction,
            MediaType.VN.value,
            caracteres,
            time_spent_min,
            nombre,
            comentario,
            backlog,
        )

    @log_group.command(name="ln", description="Registra progreso en una LN")
    @app_commands.describe(caracteres="Número de caracteres leídos")
    @app_commands.describe(
        tiempo="""Tiempo estimado que ha estado leyendo. Formatos aceptados: 01:20, 20, 20min, 1h"""
    )
    @app_commands.describe(nombre="""Nombre de la LN""")
    @app_commands.describe(comentario="""Comentario extra a registrar""")
    @app_commands.describe(
        backlog="""Registra en un día anterior. Formato aceptado: [yyyy-mm-dd]. Ejemplo: 2024-02-01"""
    )
    async def log_ln(
        self,
        interaction: discord.Interaction,
        caracteres: int,
        tiempo: str,
        nombre: str,
        comentario: Optional[str],
        backlog: Optional[str],
    ):
        await interaction.response.defer()

        if caracteres > 200000:
            return await interaction.edit_original_response(
                content="No se pueden registrar más de 200000 caracteres de una vez."
            )
        if caracteres < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        time_spent_min = helpers.elapsed_time_to_mins(tiempo)
        if time_spent_min < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        return await self.log(
            interaction,
            MediaType.LN.value,
            caracteres,
            time_spent_min,
            nombre,
            comentario,
            backlog,
        )

    @log_group.command(
        name="game", description="Registra minutos jugados a un videojuego"
    )
    @app_commands.describe(
        tiempo="""Tiempo estimado que ha estado jugando. Formatos aceptados: 01:20, 20, 20min, 1h"""
    )
    @app_commands.describe(
        nombre="""Nombre del videojuego. Para VNs o juegos centrados en texto use /log vn"""
    )
    @app_commands.describe(comentario="""Comentario extra a registrar""")
    @app_commands.describe(
        backlog="""Registra en un día anterior. Formato aceptado: [yyyy-mm-dd]. Ejemplo: 2024-02-01"""
    )
    async def log_game(
        self,
        interaction: discord.Interaction,
        tiempo: str,
        nombre: str,
        comentario: Optional[str],
        backlog: Optional[str],
    ):
        await interaction.response.defer()

        time_spent_min = helpers.elapsed_time_to_mins(tiempo)
        if time_spent_min > 480:
            return await interaction.edit_original_response(
                content="No se pueden registrar más de 480 minutos de una vez."
            )
        if time_spent_min < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        return await self.log(
            interaction,
            MediaType.GAME.value,
            time_spent_min,
            time_spent_min,
            nombre,
            comentario,
            backlog,
        )

    @log_group.command(name="audiobook", description="Registra minutos de Audiolibro")
    @app_commands.describe(
        tiempo="""Tiempo estimado que ha estado escuchando el audiolibro. Formatos aceptados: 01:20, 20, 20min, 1h"""
    )
    @app_commands.describe(nombre="""Nombre del audiolibro""")
    @app_commands.describe(comentario="""Comentario extra a registrar""")
    @app_commands.describe(
        backlog="""Registra en un día anterior. Formato aceptado: [yyyy-mm-dd]. Ejemplo: 2024-02-01"""
    )
    async def log_audiobook(
        self,
        interaction: discord.Interaction,
        tiempo: str,
        nombre: str,
        comentario: Optional[str],
        backlog: Optional[str],
    ):
        await interaction.response.defer()

        time_spent_min = helpers.elapsed_time_to_mins(tiempo)
        if time_spent_min > 480:
            return await interaction.edit_original_response(
                content="No se pueden registrar más de 480 minutos de una vez."
            )
        if time_spent_min < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        return await self.log(
            interaction,
            MediaType.AUDIOBOOK.value,
            time_spent_min,
            time_spent_min,
            nombre,
            comentario,
            backlog,
        )

    @log_group.command(name="listening", description="Registra minutos de listening")
    @app_commands.describe(
        tiempo="""Tiempo estimado que ha estado escuchando contenido. Formatos aceptados: 01:20, 20, 20min, 1h"""
    )
    @app_commands.describe(nombre="""Nombre de la VN""")
    @app_commands.describe(comentario="""Comentario extra a registrar""")
    @app_commands.describe(
        backlog="""Registra en un día anterior. Formato aceptado: [yyyy-mm-dd]. Ejemplo: 2024-02-01"""
    )
    async def log_listening(
        self,
        interaction: discord.Interaction,
        tiempo: str,
        nombre: str,
        comentario: Optional[str],
        backlog: Optional[str],
    ):
        await interaction.response.defer()

        time_spent_min = helpers.elapsed_time_to_mins(tiempo)
        if time_spent_min > 480:
            return await interaction.edit_original_response(
                content="No se pueden registrar más de 480 minutos de una vez."
            )
        if time_spent_min < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        return await self.log(
            interaction,
            MediaType.LISTENING.value,
            time_spent_min,
            time_spent_min,
            nombre,
            comentario,
            backlog,
        )

    @log_group.command(name="readtime", description="Registra minutos de lectura")
    @app_commands.describe(
        tiempo="""Tiempo estimado que ha estado escuchando contenido. Formatos aceptados: 01:20, 20, 20min, 1h"""
    )
    @app_commands.describe(nombre="""Nombre del libro""")
    @app_commands.describe(comentario="""Comentario extra a registrar""")
    @app_commands.describe(
        backlog="""Registra en un día anterior. Formato aceptado: [yyyy-mm-dd]. Ejemplo: 2024-02-01"""
    )
    async def log_readtime(
        self,
        interaction: discord.Interaction,
        tiempo: str,
        nombre: str,
        comentario: Optional[str],
        backlog: Optional[str],
    ):
        await interaction.response.defer()

        time_spent_min = helpers.elapsed_time_to_mins(tiempo)
        if time_spent_min > 480:
            return await interaction.edit_original_response(
                content="No se pueden registrar más de 480 minutos de una vez."
            )
        if time_spent_min < 0:
            return await interaction.edit_original_response(
                content="Solo se permiten números positivos."
            )

        return await self.log(
            interaction,
            MediaType.READTIME.value,
            time_spent_min,
            time_spent_min,
            nombre,
            comentario,
            backlog,
        )

    async def log(
        self,
        interaction: discord.Interaction,
        media_type: str,
        amount: int,
        time: int,
        name: Optional[str],
        comment: Optional[str],
        backlog: Optional[str],
    ):
        if interaction.channel.id != channelid:
            return await interaction.edit_original_response(
                content="Solo puedes logear en el canal #registro-inmersión."
            )

        print(
            f"[LOGGING FOR {interaction.user.name}]: {media_type} - {amount}u - {time} mins - {name} - {comment} - {backlog}"
        )

        if amount in [float("inf"), float("-inf")]:
            return await interaction.edit_original_response(
                content="No se permite infinito."
            )

        if backlog:
            now = datetime.now()
            created_at = datetime.now().replace(
                year=int(backlog.split("-")[0]),
                month=int(backlog.split("-")[1]),
                day=int(backlog.split("-")[2]),
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
            if now < created_at:
                return await interaction.edit_original_response(
                    content="""No puedes registrar logs en el futuro."""
                )
            if now > created_at:
                date = created_at
        if not backlog:
            date = datetime.now()

        def check_achievements(discord_user_id, media_type):
            logs = store.get_logs_by_user(discord_user_id, media_type, None)
            weighed_points_mediums = helpers.multiplied_points(logs)
            abmt = helpers.calc_achievements(weighed_points_mediums)
            if not bool(abmt):
                return 0, 0, 0, "", "", "", ""
            (
                lower_interval,
                current_points,
                upper_interval,
                rank_emoji,
                rank_name,
                next_rank_emoji,
                next_rank_name,
            ) = helpers.get_achievemnt_index(abmt)

            return (
                lower_interval,
                current_points,
                upper_interval,
                rank_emoji,
                rank_name,
                next_rank_emoji,
                next_rank_name,
            )

        store = Set_Goal(os.environ["GOALS_DB_PATH"])
        then = date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(
            days=1
        )
        now = interaction.created_at.replace(hour=0, minute=0, second=0, microsecond=0)

        goals = store.get_goals(
            interaction.user.id, (now, date)
        ) + store.get_daily_goals(
            interaction.user.id
        )  # getting goals for the current day and daily goals
        point_goals = store.get_point_goals(
            interaction.user.id, (now, date)
        )  # getting point goals

        store = Store(os.environ["PROD_DB_PATH"])
        first_date = date.replace(day=1, hour=0, minute=0, second=0)
        calc_amount, format, msg, title = helpers.point_message_converter(
            media_type.upper(), amount, name
        )
        # returns weighed amount (i.e 1ep = 9.5 so weighed amount of 1 ANIME EP is 9.5), format (i.e chars, pages, etc), msg i.e 1/350 points/characters = x points, title is the anime/vn/manga title through anilist or vndb query
        old_points = store.get_logs_by_user(
            interaction.user.id, None, (first_date, date)
        )  # query to get logs of past month for monlthy point overview i.e ~~June: 2k~~ -> June: 2.1k

        old_weighed_points_mediums = helpers.multiplied_points(old_points)
        (
            old_rank_achievement,
            old_achievemnt_points,
            old_next_achievement,
            old_emoji,
            old_rank_name,
            old_next_rank_emoji,
            old_next_rank_name,
        ) = check_achievements(interaction.user.id, media_type.upper())
        # returns achievemnt progress before log is getting registered to compare with achievement progress after log

        store.new_log(
            interaction.guild_id,
            interaction.user.id,
            media_type.upper(),
            amount,
            time,
            [title, comment],
            date,
        )  # log being registered

        (
            current_rank_achievement,
            current_achievemnt_points,
            new_rank_achievement,
            new_emoji,
            new_rank_name,
            new_next_rank_emoji,
            new_next_rank_name,
        ) = check_achievements(interaction.user.id, media_type.upper())
        # getting new achievement progress

        print(f"11111111111 {amount}")
        current_points = store.get_logs_by_user(
            interaction.user.id, None, (first_date, date)
        )  # current total points
        current_weighed_points_mediums = helpers.multiplied_points(current_points)

        recent_logs = store.get_recent_goal_alike_logs(
            interaction.user.id, (now, date)
        )  # getting logs of past day for goals

        async def goals_row(
            discord_user_id, req_media_type, req_amount, text, created_at, frequency
        ):
            for log in recent_logs:
                if log.media_type.value == req_media_type:
                    if title == text:
                        return f"""- {"~~" + str(log.amount) + "/" + str(req_amount) + " " + str(helpers.media_type_format(req_media_type.value)) + " " + text + "~~" if log.amount >= req_amount else str(log.amount) + "/" + req_amount + str(helpers.media_type_format(req_media_type.value)) + text}"""
                    if title != text:
                        return

        goals_description = []

        rl_notes_l = [note for media_type, amount, note in recent_logs]
        rl_media_type_l = [media_type for media_type, amount, note in recent_logs]
        rl_media_type_amount_l = [
            (media_type, amount) for media_type, amount, note in recent_logs
        ]
        # handling goals, i.e watch 3 eps of anime, read 3000 chars of VN by comparing two lists (goals and recent_logs)
        if goals:
            for goals_row in goals:
                if recent_logs:
                    if any(goals_row.text in text for text in rl_notes_l):
                        indices = helpers.indices_text(recent_logs, goals_row.text)
                        points = []
                        for i in indices:
                            points.append(recent_logs[i].da)
                        goals_description.append(
                            f"""- {"~~" + str(int(sum(points))) + "/" + str(int(goals_row.amount)) + " " + str(helpers.media_type_format(goals_row.media_type.value)) + " " + goals_row.text + "~~" if sum(points) >= goals_row.amount else str(int(sum(points))) + "/" + str(int(goals_row.amount)) + " " + str(helpers.media_type_format(goals_row.media_type.value)) + " " + goals_row.text} {"(" + goals_row.freq + ")" if goals_row.freq != None else ""}"""
                        )
                        continue
                    else:
                        goals_description.append(
                            f"""- 0/{goals_row.amount} {helpers.media_type_format(goals_row.media_type.value)} {goals_row.text} {"(" + goals_row.freq + ")" if goals_row.freq != None else ""}"""
                        )
                        break
                else:
                    goals_description.append(
                        f"""- 0/{goals_row.amount} {helpers.media_type_format(goals_row.media_type.value)} {goals_row.text} {"(" + goals_row.freq + ")" if goals_row.freq != None else ""}"""
                    )
                    continue

        print(f"222222 {amount}")

        # handling point_goals
        if point_goals:
            for points_row in point_goals:
                if recent_logs:
                    if points_row.media_type in rl_media_type_l:
                        indices = helpers.indices_media(
                            recent_logs, points_row.media_type
                        )
                        points = []
                        for i in indices:
                            points.append(
                                helpers._to_amount(
                                    recent_logs[i].media_type.value, recent_logs[i].da
                                )
                            )
                        goals_description.append(
                            f"""- {sum(points)}/{points_row.amount} puntos {points_row.text} {"(" + points_row.freq + ")" if points_row.freq != None else ""}"""
                        )
                        continue
                    else:
                        if points_row.media_type.value == "ANYTHING":
                            points = []
                            for media, amount2 in rl_media_type_amount_l:
                                points.append(helpers._to_amount(media.value, amount2))
                            goals_description.append(
                                f"""- {"~~" + str(round(sum(points), 0)) + "/" + str(points_row.amount2) + " puntos " + points_row.text + (" (" + points_row.freq + ") " if points_row.freq != None else "") + "~~" if sum(points) >= points_row.amount else str(round(sum(points), 0)) + "/" + str(points_row.amount) + " puntos " + points_row.text + (" (" + points_row.freq + ") " if points_row.freq != None else "")}"""
                            )
                            continue
                        else:
                            goals_description.append(
                                f"""- 0/{points_row.amount} puntos {points_row.text} {"(" + points_row.freq + ")" if points_row.freq != None else ""}"""
                            )
                            break
                else:
                    goals_description.append(
                        f"""- 0/{points_row.amount} puntos {points_row.text} {"(" + points_row.freq + ")" if points_row.freq != None else ""}"""
                    )
                    continue
        goals_description = "\n".join(goals_description)
        print(goals_description)

        # final log message
        await interaction.edit_original_response(
            content=f'''### {interaction.user.mention} ha logeado {amount} {format} de {title} en {time} minutos\n{msg}\n\n{"""__**Objetivos:**__
""" + str(goals_description) + """
""" if goals_description else ""}**{date.strftime("%B").title()}:** ~~{helpers.millify(sum(i for i, j in list(old_weighed_points_mediums.values())))}~~ → **{helpers.millify(sum(i for i, j in list(current_weighed_points_mediums.values())))}**\n{"""
**Siguiente logro: **""" + new_next_rank_name + " " + new_next_rank_emoji + " en " + str(new_rank_achievement-current_achievemnt_points) + " " + helpers.media_type_format(media_type.upper()) if old_next_achievement == new_rank_achievement else """
**Logro desbloqueado!: **""" + new_rank_name + " " + new_emoji + " " + str(int(current_rank_achievement)) + " " + helpers.media_type_format(media_type.upper()) + """
**Siguiente logro:** """ + new_next_rank_name + " " + new_next_rank_emoji + " " + str(int(new_rank_achievement)) + " " + helpers.media_type_format(media_type.upper())}\n\n{">>> " + comment if comment else ""}'''
        )

    @log_anime.autocomplete("nombre")
    async def log_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        print("Autocompleting")
        media_type = interaction.namespace["media_type"]
        suggestions = []
        url = ""

        return []
        #
        # if media_type == "VN":
        #     url = "https://api.vndb.org/kana/vn"
        #     data = {
        #         "filters": ["search", "=", f"{current}"],
        #         "fields": "title, alttitle",
        #     }  # default no. of results is 10
        #
        # elif media_type == "Anime" or media_type == "Manga":
        #     url = "https://graphql.anilist.co"
        #     query = f"""
        #     query ($page: Int, $perPage: Int, $title: String) {{
        #         Page(page: $page, perPage: $perPage) {{
        #             pageInfo {{
        #                 total
        #                 perPage
        #             }}
        #             media (search: $title, type: {media_type.upper()}) {{
        #                 id
        #                 title {{
        #                     romaji
        #                     native
        #                 }}
        #             }}
        #         }}
        #     }}
        #     """
        #
        #     variables = {"title": current, "page": 1, "perPage": 10}
        #
        #     data = {"query": query, "variables": variables}
        #
        # if not url:
        #     return []
        #
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(url, json=data) as resp:
        #         log.info(resp.status)
        #         json_data = await resp.json()
        #
        #         if media_type == "VN":
        #             suggestions = [
        #                 (result["title"], result["id"])
        #                 for result in json_data["results"]
        #             ]
        #
        #         elif media_type == "Anime" or media_type == "Manga":
        #             suggestions = [
        #                 (
        #                     f"{result['title']['romaji']} ({result['title']['native']})",
        #                     result["id"],
        #                 )
        #                 for result in json_data["data"]["Page"]["media"]
        #             ]
        #
        #         await asyncio.sleep(0)
        #
        #         return [
        #             app_commands.Choice(name=title, value=str(id))
        #             for title, id in suggestions
        #             if current.lower() in title.lower()
        #         ]
        #


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Log(bot))
