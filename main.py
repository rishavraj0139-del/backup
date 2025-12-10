import json, os, asyncio
from telethon import TelegramClient

api_id = 32851401
api_hash = "b4811a9dbe8ebfafd461005d02b5920e"

source_chat = -1002823119932       # replace with your correct ID
destination_chat = -1003256969691  # replace with your correct ID

session_name = "backup.session"     # YOUR session file
progress_file = "progress.json"

async def main():
    client = TelegramClient("backup", api_id, api_hash)
    await client.start()
    print("Logged in successfully...")

    # Load last processed message
    last_id = 0
    if os.path.exists(progress_file):
        last_id = json.load(open(progress_file)).get("last_id", 0)

    print(f"Starting from message ID > {last_id}")

    async for msg in client.iter_messages(source_chat, min_id=last_id):
        # Save last message ID
        json.dump({"last_id": msg.id}, open(progress_file, "w"))

        if msg.media:
            file_path = await msg.download_media()
            await client.send_file(destination_chat, file_path,
                                   caption=msg.text or "")
            print(f"[MEDIA] {msg.id} uploaded")

        elif msg.text:
            await client.send_message(destination_chat, msg.text)
            print(f"[TEXT] {msg.id} uploaded")

    print("Backup completed!")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
