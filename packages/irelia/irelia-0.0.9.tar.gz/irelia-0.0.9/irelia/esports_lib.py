# Scripts for importing the files
import requests
import datetime

headers = {'x-api-key': '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'}
params = {"hl": "en-US"}
s11_start_date = "2021-01-01"


class Lolesports:
    def get_leagues(self):
        return requests.get('https://esports-api.lolesports.com/persisted/gw/getLeagues', params=params, headers=headers).json()


    def get_tournament_from_league(self, leagueId):
        params['leagueId'] = leagueId
        return requests.get('https://esports-api.lolesports.com/persisted/gw/getTournamentsForLeague', params=params, headers=headers).json()


    def get_standings(self, tournamentId):
        params['tournamentId'] = tournamentId
        return requests.get('https://esports-api.lolesports.com/persisted/gw/getStandings', params=params, headers=headers).json()


    def get_schedule(self, leagueId, pageToken=None):
        params['leagueId'] = leagueId
        if pageToken is not None:
            params['pageToken'] = pageToken
        return requests.get('https://esports-api.lolesports.com/persisted/gw/getSchedule', params=params, headers=headers).json()

    def get_full_schedule(self, leagueId, current=True):
        data = self.get_schedule(leagueId)
        if "errors" in data:
            print("getFullScheduleError")
            return leagueId
        else:
            pageTokens = []
            full_schedule = []
            while data['data']['schedule']['pages']['older'] is not None:
                full_schedule += data['data']['schedule']['events']
                pageToken = data['data']['schedule']['pages']['older']
                pageTokens.append(pageToken)
                data = self.get_schedule(leagueId, pageToken)

            full_schedule += data['data']['schedule']['events']
            pageToken = data['data']['schedule']['pages']['older']
            pageTokens.append(pageToken)
            # sort the full_schedule here with a list comprehension
            ordered_schedule = sorted(full_schedule, key=lambda k: datetime.datetime.strptime(k['startTime'], "%Y-%m-%dT%H:%M:%SZ"))
            if current is False:
                return ordered_schedule
            else:
                current_schedule = []
                for match in ordered_schedule:
                    if match['startTime'] >= s11_start_date:
                        current_schedule.append(match)
                return current_schedule

    def get_event_details(self, matchId):
        params['id'] = matchId
        return requests.get("https://esports-api.lolesports.com/persisted/gw/getEventDetails", params=params, headers=headers).json()

    def get_completed_events(self, tournamentId):
        params['tournamentId'] = tournamentId
        return requests.get("https://esports-api.lolesports.com/persisted/gw/getCompletedEvents", params=params, headers=headers).json()

    def get_teams(self, teamId):
        params['id'] = teamId
        return requests.get('https://esports-api.lolesports.com/persisted/gw/getTeams', params = params, headers = headers).json()['data']['teams']

    def get_all_teams(self):
        return requests.get('https://esports-api.lolesports.com/persisted/gw/getTeams', params = params, headers = headers).json()['data']['teams']

'''
    # datetime format: 2020-09-25T12:43:00Z (YYYY-MM-dd'T'hh-mm-ss'Z')
    def get_full_game_window(self, gameId, startingTime):
        master_window = {}
        window = self.get_window(gameId, startingTime)
        start_date = datetime.datetime.strptime(startingTime, '%Y-%m-%dT%H:%M:%SZ')
        formatted_start = ''
        valid_start = False
        if window.status_code == 204:
            pass
            # print("not ok")
        elif window.status_code == 404:
            print("Not valid game")
            return None
        else:
            valid_start = True

        # games don't start exactly at the scheduled time
        while valid_start is not True:
            start_date += datetime.timedelta(seconds=20)
            print(start_date)
            formatted_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            window = self.get_window(gameId, formatted_date)
            if window.status_code == 204:
                pass
            elif window.status_code == 400:
                break
            else:
                print("ok")
                valid_start = True
                formatted_start = formatted_date

        # storing variables in the master dict
        master_window['start_date'] = formatted_start
        master_window['esportsGameId'] = window.json()['esportsGameId']
        master_window['esportsMatchId'] = window.json()['esportsMatchId']
        master_window['gameMetadata'] = window.json()['gameMetadata']
        master_window['frames'] = window.json()['frames']

        current_time = start_date
        finished = False
        # iterating until you've reached the last frame
        while finished is False:
            current_time += datetime.timedelta(seconds=100)
            formatted_date = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            window = self.get_window(gameId, formatted_date)
            for frame in window.json()['frames']:
                if frame['gameState'] == 'in_game':
                    master_window['frames'].append(frame)
                elif frame['gameState'] == 'finished':
                    master_window['frames'].append(frame)
                    master_window['finished_time'] = frame['rfc460Timestamp']
                    finished = True

        return master_window



    # datetime format: 2020-09-25T12:43:00Z (YYYY-MM-dd'T'hh-mm-ss'Z')
    def get_window(gameId, startingTime=None):
        params['gameId'] = gameId
        if startingTime is not None:
            params['startingTime'] = startingTime
        else:
            params['startingTime'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        return requests.get("https://feed.lolesports.com/livestats/v1/window/{0}".format(gameId), params=params, headers=headers)


'''
