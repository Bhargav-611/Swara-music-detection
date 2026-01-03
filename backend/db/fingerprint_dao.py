from backend.db.connection import get_connection


class FingerprintDAO:

    @staticmethod
    def insert_song(title, artist, audio_url=None):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO songs (title, artist, audio_url)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (title, artist, audio_url)
        )

        song_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return song_id


    @staticmethod
    def insert_fingerprints(song_id, fingerprints):
        conn = get_connection()
        cur = conn.cursor()

        cur.executemany(
            "INSERT INTO fingerprints (hash, song_id, time_offset) VALUES (%s, %s, %s)",
            [(h, song_id, float(t)) for h, t in fingerprints]
        )

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def query_hash(hash_value):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT song_id, time_offset FROM fingerprints WHERE hash = %s",
            (hash_value,)
        )

        results = cur.fetchall()

        cur.close()
        conn.close()

        return results
