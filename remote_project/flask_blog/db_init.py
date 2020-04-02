from app import database, Entry, FTSEntry

if __name__ == '__main__':
    database.create_tables([Entry, FTSEntry], safe=True)
