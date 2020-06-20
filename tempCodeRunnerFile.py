
        if not existKey(key, self.guilds):
            self.guildManagers[key] = GuildManager(key)