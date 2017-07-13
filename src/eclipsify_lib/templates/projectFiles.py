from generator import ProjectFile as PF

files = ( PF('.project'), PF('.cproject'),  PF('language.settings.xml', ['.settings']) );
