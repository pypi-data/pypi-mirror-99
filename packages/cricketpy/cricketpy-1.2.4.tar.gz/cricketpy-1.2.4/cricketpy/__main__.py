from pyfiglet import Figlet
import math
import os
from criapi import Cricbuzz
from rich.console import Console
from rich.table import Table
from rich import box

def get_score_row(match):
    score = match
    separator = ' & '
    score_row = ""
    if len(score['batting']['score']):
        batting = score['batting']['score']
        board = []

        for bat in batting:
            if 'overs' in bat:
                board.append(bat['runs']+'-'+bat['wickets']+'('+bat['overs']+')')
            else:
                board.append(bat['runs']+'-'+bat['wickets'])
        
        batting_score = separator.join(board)
        score_row = score['batting']['team']+': '+batting_score
    else:
        score_row = score['batting']['team']+': '
    if score['bowling']['score']!=[{}]:
        bowling = score['bowling']['score']
        bboard = []

        for bowl in bowling:
            if 'overs' in bowl:
                bboard.append(bowl['runs']+'-'+bowl['wickets']+'('+bowl['overs']+')')
            else:
                board.append(bowl['runs']+'-'+bowl['wickets'])
        
        bowling_score = separator.join(bboard)
        score_row += '\n' + score['bowling']['team']+': '+bowling_score
    else:
        score_row += '\n'+score['bowling']['team']+': '
    score_row += '\n'+match['status']
    return score_row

def print_scores(matches):
        console = Console()
        os.system( 'clear' )
        score_table=Table(show_header=False,show_lines=True)
        score_table.add_column()
        for match in matches:
            score_table.add_row(get_score_row(match))
        score_table.add_row('match number:commentary,q:quit,r:refresh')
        console.print(score_table)


def get_batsmen_row(batsmen,batsmen_table):
    name=batsmen['name']
    runs=batsmen['runs']
    balls=batsmen['balls']
    fours=batsmen['fours']
    six=batsmen['six']
    sr=batsmen['sr']
    if 'dismissal' in batsmen:
        dismissal=batsmen['dismissal']
        batsmen_table.add_row(name,dismissal,runs, balls, fours,six,sr)
    else:
        batsmen_table.add_row(name,runs, balls, fours,six,sr)
    return batsmen_table

def get_bowler_row(bowler,bowler_table):
    name=bowler['name']
    overs=bowler['overs']
    maidens=bowler['maidens']
    runs=bowler['runs']
    wickets=bowler['wickets']
    balls=str((math.floor(float(overs))*6+math.floor((float(overs)-math.floor(float(overs)))*10))/6)
    if balls=="0":
        er='0'
    else:
        er=str(round(int(runs)/float(balls),2))
    bowler_table.add_row(name,overs,maidens,runs,wickets,er)
    return bowler_table

def get_commentary_row(comment,commentary_table):
    comm=comment['comm']
    over=comment['over']
    comm=comm.replace('<strong>','[bold]')
    comm=comm.replace('</strong>','[/bold]')
    comm=comm.replace('<b>','[bold]')
    comm=comm.replace('</b>','[/bold]')
    comm=comm.replace('<br/>','\n')
    comm=comm.replace('<i>','[italic]')
    comm=comm.replace('</i>','[/italic]')
    comm=comm.replace('<span class="over-summary">','')
    comm=comm.replace('</span>','')
    if comm[0:2]=='<a':
        return commentary_table
    elif over==None:
        commentary_table.add_row(comm)
    else:
        commentary_table.add_row(over+': '+comm)
    return commentary_table

def cricpy():
    c=Cricbuzz()
    f = Figlet(font='slant')
    console=Console()
    print(f.renderText('CRICPY'))
    while 1:
        matches=c.livescore()
        print_scores(matches)
        choice=input()
        if choice=='q':
            os.system( 'clear' )
            exit()
        elif choice=='r':
            continue
        else :
            while 1:
                os.system( 'clear' )
                matches=c.livescore()
                match=matches[int(choice)-1]
                single_score_table=Table(show_header=False,show_lines=True)
                single_score_table.add_column()
                single_score_table.add_row(get_score_row(match))
                console.print(single_score_table)
                commentary=c.commentary(match['id'])

                if len(commentary['batsman']):
                    batsmens=commentary['batsman']
                    current_batsmen_table=Table("Batsman", "R", "B", "4s","6s","SR")
                    for batsmen in batsmens:
                        current_batsmen_table=get_batsmen_row(batsmen,current_batsmen_table)
                    console.print(current_batsmen_table)
                    current_bowler_table=Table("Bowler", "O", "M", "R","W","ER")
                    bowler=commentary['bowler'][0]
                    current_bowler_table=get_bowler_row(bowler,current_bowler_table)
                    console.print(current_bowler_table)

                commentary=commentary['comm']
                commentary_table=Table(show_header=False,padding=(1,0,0,0))
                for comment in commentary:
                    commentary_table=get_commentary_row(comment,commentary_table)
                commentary_table.add_row('s:scorecard,b:back,r:refresh,q:quit')
                console.print(commentary_table)

                ch=input()
                if ch=='r':
                    continue
                elif ch=='b':
                    break
                elif ch=='q':
                    os.system( 'clear' )
                    exit()
                elif ch=='s':
                    scorecard=c.scorecard(match['id'])
                    inning=scorecard[0]
                    while 1:
                        os.system( 'clear' )
                        batsmens=inning['batcard']

                        batsmen_table=Table("Batsman","Dismissal", "R", "B", "4s","6s","SR")
                        for batsmen in batsmens:
                            batsmen_table=get_batsmen_row(batsmen,batsmen_table)
                        console.print(batsmen_table)

                        bowler_table=Table("Bowler", "O", "M", "R","W","ER")
                        bowlers=inning['bowlcard']
                        for bowl in bowlers:
                            bowler_table=get_bowler_row(bowl,bowler_table)
                        console.print(bowler_table)

                        fall_wickets_table=Table("Fall of Wickets", "Score", "Over")
                        fall_wickets=inning['fall_wickets']
                        for fall_wicket in fall_wickets:
                            name=fall_wicket['name']
                            wicket=fall_wicket['wkt_num']
                            score=fall_wicket['score']
                            overs=fall_wicket['overs']
                            score=score+'-'+wicket
                            fall_wickets_table.add_row(name,score,overs)
                        console.print(fall_wickets_table)
                        print('inning number:inning scorecard,b:back,r:refresh,q:quit')

                        chh=input()
                        if chh=='b':
                            break
                        elif chh=='r':
                            continue
                        elif chh=='q':
                            os.system( 'clear' )
                            exit()
                        else:
                            try:
                                inning=scorecard[int(chh)-1]
                            except:
                                print("wrong innings")
                            continue


if __name__=="__main__":
    cricpy()
