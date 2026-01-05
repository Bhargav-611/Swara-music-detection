import io
import binascii
from db.connection import get_connection


class FingerprintDAO:

    def hex_to_bytes(h):
        # h may be escaped-string or hex-string
        if h.startswith("\\x"):
            h = h[2:]
        return bytes.fromhex(h)

    @staticmethod
    def insert_song(title, audio_url=None):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO songs (title, audio_url)
            VALUES (%s, %s)
            RETURNING id
            """,
            (title, audio_url)
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

        buffer = io.StringIO()

        for h, t in fingerprints:
            # 🔴 h looks like '\xf6\x85\xc9...'
            # Convert it to HEX safely
            hex_hash = h.encode("latin1").hex()

            buffer.write(
                f"\\x{hex_hash}\t{int(song_id)}\t{float(t)}\n"
            )
        print(repr(buffer.getvalue().splitlines()[0]))

        buffer.seek(0)
        print(repr(buffer.getvalue().splitlines()[0]))

        cur.copy_from(
            buffer,
            "fingerprints",
            sep="\t",
            columns=("hash", "song_id", "time_offset")
        )

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def query_hash(hash_value):
        conn = get_connection()
        cur = conn.cursor()

        hash_bytes = bytes.fromhex(hash_value)

        cur.execute(
            "SELECT song_id, time_offset FROM fingerprints WHERE hash = %s",
            (hash_bytes,)
        )

        results = cur.fetchall()
        cur.close()
        conn.close()

        return results


    @staticmethod
    def get_song_by_id(song_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, title, audio_url FROM songs WHERE id = %s",
            (song_id,)
        )

        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return {
                "id": result[0],
                "title": result[1],
                "audio_url": result[2]
            }
        return None

    @staticmethod
    def get_song_by_url(audio_url):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, title, audio_url FROM songs WHERE audio_url = %s",
            (audio_url,)
        )

        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return {
                "id": result[0],
                "title": result[1],
                "audio_url": result[2]
            }
        return None
    
    @staticmethod
    def query_hashes_bulk(hash_list):
        """
        hash_list: list of HEX STRINGS
        """
        conn = get_connection()
        cur = conn.cursor()

        hash_bytes_list = [bytes.fromhex(h) for h in hash_list]

        query = """
            SELECT hash, song_id, time_offset
            FROM fingerprints
            WHERE hash = ANY(%s)
        """

        cur.execute(query, (hash_bytes_list,))
        results = cur.fetchall()

        cur.close()
        conn.close()

        return results
