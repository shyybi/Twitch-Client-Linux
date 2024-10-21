import requests
import tkinter as tk
from tkinter import ttk
CLIENT_ID = "oi0rtnk972zackbs4dzimsiwycdh9f"
CLIENT_SECRET = "pt5q7ao0xk56x0cxwxnvxnb3ax5kjo"

def get_oauth_token():
    url = f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials"
    response = requests.post(url)
    return response.json()['access_token']

def get_top_streams(limit=10):
    url = f"https://api.twitch.tv/helix/streams?first={limit}"
    
    oauth_token = get_oauth_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {oauth_token}'
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur: {response.status_code}")
        return None

class TwitchApp:
    def __init__(self, master):
        self.master = master
        master.title("Top Streams Twitch")
        master.geometry("600x400")

        self.tree = ttk.Treeview(master, columns=('Chaîne', 'Jeu', 'Spectateurs'), show='headings')
        self.tree.heading('Chaîne', text='Chaîne')
        self.tree.heading('Jeu', text='Jeu')
        self.tree.heading('Spectateurs', text='Spectateurs')
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.refresh_button = tk.Button(master, text="Rafraîchir", command=self.refresh_streams)
        self.refresh_button.pack()

    def refresh_streams(self):
        self.tree.delete(*self.tree.get_children())
        top_streams = get_top_streams()
        if top_streams and 'data' in top_streams:
            for stream in top_streams['data']:
                self.tree.insert('', 'end', values=(
                    stream['user_name'],
                    stream['game_name'],
                    stream['viewer_count']
                ))
        else:
            print("Impossible de récupérer les streams")

if __name__ == "__main__":
    root = tk.Tk()
    app = TwitchApp(root)
    root.mainloop()
