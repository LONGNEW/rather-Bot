import discord, datetime, parsing as tool, pytz, asyncio
from discord.ext import tasks, commands

def status():
    print(f"now running {asyncio.get_running_loop()}")

class MyCog(commands.Cog):
    def __init__(self):
        self.channels = dict()
        self.info = [dict() for _ in range(4)]
        self.prev_date = "22.02.09"
        self.notice.start()

    @tasks.loop(minutes=3)
    async def notice(self):

        where = ["백마 광장", "학사 공지", "일반 소식", "사업단 소식"]

        KST = pytz.timezone("Asia/Seoul")
        withtime = str(datetime.datetime.now(KST)).replace("-", ".")[2:].split()
        date = withtime[0]
        time = withtime[1].split(".")[0]

        if date != self.prev_date:
            self.info = [dict() for _ in range(4)]
            self.prev_date = date

        uploaded = []
        for i in range(4):
            # ret[0] has a value that how many posts are uploaded in today
            ret, cnt = tool.what_you_want(i, date), 0
            temp = discord.Embed(title=where[i], description=ret[0], color=0x62c1cc)

            uploaded.append(str(ret[0]).strip())
            for j in range(1, len(ret)):
                title = ret[j][1]
                if title in self.info[i]:
                    continue

                cnt += 1
                self.info[i][title] = 1
                title = str(ret[j][0] + "    " + ret[j][1])
                temp.add_field(name=title, value=ret[j][-1], inline=False)
                
            await ch.channel.send("", embed=temp)

            if cnt:
                for ch in self.channels:
                    print(f"send to : {ch.guild, ch.id}")
                    await ch.send("", embed=temp)

        print(f"Update : {uploaded}")
