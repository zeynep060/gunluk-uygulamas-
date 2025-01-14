import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import json
from datetime import datetime
import random

# Kullanıcı adını JSON dosyasından almak için fonksiyon
def get_username():
    try:
        with open("user_info.json", "r") as file:
            user_info = json.load(file)
            return user_info.get("username", None)
    except FileNotFoundError:
        return None

# Kullanıcı adını JSON dosyasına kaydetmek için fonksiyon
def save_username(username):
    user_info = {"username": username}
    with open("user_info.json", "w") as file:
        json.dump(user_info, file)

# Bir frame'i göstermek ve önceki frame'i gizlemek için fonksiyon
def show_frame(frame):
    global previous_frame
    if previous_frame is not None:
        previous_frame.pack_forget()
    frame.pack(fill='both', expand=True, padx=10, pady=10)
    previous_frame = frame

# Günlük yazısını JSON dosyasına kaydetmek için fonksiyon
def save_entry():
    title = entry_title.get().strip()
    entry = entry_text.get("1.0", tk.END).strip()
    if title and entry:
        date_str = datetime.now().strftime("%Y-%m-%d")
        diary_entry = {"date": date_str, "title": title, "entry": entry}
        try:
            with open("diary.json", "r") as file:
                diary = json.load(file)
        except FileNotFoundError:
            diary = []
        diary.append(diary_entry)
        with open("diary.json", "w") as file:
            json.dump(diary, file, indent=4)
        messagebox.showinfo("Başarılı", "Günlük yazısı başarıyla kaydedildi!")
        entry_title.delete(0, tk.END)
        entry_text.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Uyarı", "Başlık ve günlük yazısı boş olamaz!")

# Günlük yazısı frame'ini göstermek için fonksiyon
def show_diary_frame():
    show_frame(diary_frame)

# Rastgele bir günlük yazısını hatırlatmak için fonksiyon
def recall_memory():
    memory_frame = tk.Frame(main_frame, bg='#E6E6FA')  # Lavanta rengi
    
    try:
        with open("diary.json", "r") as file:
            diary = json.load(file)
    except FileNotFoundError:
        diary = []
    
    if not diary:
        memory_label = tk.Label(memory_frame, text="Henüz hiçbir günlük yazmadınız!", wraplength=350, bg='#E6E6FA', fg='#4B0082', font=font)
        memory_label.pack(pady=10)
    else:
        random_entry = random.choice(diary)
        memory_label = tk.Label(memory_frame, text=f"Tarih: {random_entry['date']}\nBaşlık: {random_entry['title']}\n\n{random_entry['entry']}", wraplength=350, bg='#E6E6FA', fg='#4B0082', font=font)
        memory_label.pack(pady=10)
    
    show_frame(memory_frame)

# Zaman kapsülü oluşturma frame'ini göstermek için fonksiyon
def time_capsule():
    capsule_frame = tk.Frame(main_frame, bg='#FFFACD')  # Limon Şifonu rengi
    
    tk.Label(capsule_frame, text="Zaman Kapsülü Başlığı (İsteğe Bağlı):", font=font, bg='#FFFACD', fg='#4B0082').pack(pady=10)
    capsule_title_entry = tk.Entry(capsule_frame, width=60, font=font)
    capsule_title_entry.pack()
    
    tk.Label(capsule_frame, text="Zaman Kapsülü Mesajı:", font=font, bg='#FFFACD', fg='#4B0082').pack(pady=10)
    capsule_message_text = tk.Text(capsule_frame, height=10, width=60, font=font)
    capsule_message_text.pack()
    
    tk.Label(capsule_frame, text="Açılma Tarihi (YYYY-MM-DD):", font=font, bg='#FFFACD', fg='#4B0082').pack(pady=10)
    capsule_date_entry = tk.Entry(capsule_frame, font=font)
    capsule_date_entry.pack()

    # Zaman kapsülü verilerini JSON dosyasına kaydetmek için fonksiyon
    def save_capsule():
        title = capsule_title_entry.get().strip()
        message = capsule_message_text.get("1.0", tk.END).strip()
        open_date = capsule_date_entry.get().strip()
        try:
            datetime.strptime(open_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Uyarı", "Geçersiz tarih formatı. YYYY-MM-DD şeklinde bir tarih girin.")
            return
        if message and open_date:
            capsule = {"title": title, "message": message, "open_date": open_date, "created_date": datetime.now().strftime("%Y-%m-%d")}
            try:
                with open("time_capsules.json", "r") as file:
                    capsules = json.load(file)
            except FileNotFoundError:
                capsules = []
            capsules.append(capsule)
            with open("time_capsules.json", "w") as file:
                json.dump(capsules, file, indent=4)
            messagebox.showinfo("Başarılı", "Zaman kapsülü başarıyla oluşturuldu!")
            capsule_title_entry.delete(0, tk.END)
            capsule_message_text.delete("1.0", tk.END)
            capsule_date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Uyarı", "Mesaj ve açılma tarihi boş olamaz!")

    save_button = tk.Button(capsule_frame, text="Kaydet", command=save_capsule, bg='#4682B4', fg='#FFFFFF', font=font)  # Çelik Mavi rengi
    save_button.pack(pady=10)
    
    time_capsules_button = tk.Button(capsule_frame, text="Zaman Kapsüllerim", command=show_time_capsules, bg='#4682B4', fg='#FFFFFF', font=font)
    time_capsules_button.pack(pady=10)
    
    show_frame(capsule_frame)

# Geçmiş günlük yazılarını göstermek için fonksiyon
def show_past_entries():
    past_entries_frame = tk.Frame(main_frame, bg='#FFFACD')  # Limon Şifonu rengi
    
    canvas = tk.Canvas(past_entries_frame, bg='#FFFACD')
    scrollbar = tk.Scrollbar(past_entries_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#FFFACD')
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    try:
        with open("diary.json", "r") as file:
            diary = json.load(file)
    except FileNotFoundError:
        diary = []
    
    if not diary:
        entries_label = tk.Label(scrollable_frame, text="Henüz hiçbir günlük yazmadınız!", wraplength=350, bg='#FFFACD', fg='#4B0082', font=font)
        entries_label.pack(pady=10)
    else:
        for index, entry in enumerate(diary):
            title = entry.get('title', 'Başlıksız')
            entry_frame = tk.Frame(scrollable_frame, bg='#FFFACD')
            entry_button = tk.Button(entry_frame, text=f"Tarih: {entry['date']}\nBaşlık: {title}", wraplength=350, bg='#FFFACD', fg='#4B0082', anchor='w', justify='left', command=lambda i=index: show_entry_details(i), font=font)
            entry_button.pack(side="left", fill='x', expand=True)
            delete_button = tk.Button(entry_frame, text="Sil", bg='#DC143C', fg='#FFFFFF', command=lambda i=index: delete_entry(i), font=font)
            delete_button.pack(side="right", padx=5)
            entry_frame.pack(pady=5, fill='x')
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    back_button = tk.Button(past_entries_frame, text="Geri", command=show_diary_frame, bg='#F0E68C', fg='#00008B', font=font)  # Sarı rengi
    back_button.pack(side='bottom', anchor='e', padx=10, pady=10)
    
    show_frame(past_entries_frame)

# Günlük yazısını silmek için fonksiyon
def delete_entry(index):
    try:
        with open("diary.json", "r") as file:
            diary = json.load(file)
    except FileNotFoundError:
        diary = []
    
    if 0 <= index < len(diary):
        del diary[index]
        with open("diary.json", "w") as file:
            json.dump(diary, file, indent=4)
        show_past_entries()

# Günlük yazısının detaylarını göstermek için fonksiyon
def show_entry_details(index):
    try:
        with open("diary.json", "r") as file:
            diary = json.load(file)
    except FileNotFoundError:
        diary = []
    
    if 0 <= index < len(diary):
        entry = diary[index]
        details_frame = tk.Frame(main_frame, bg='#FFFACD')
        
        title = entry.get('title', 'Başlıksız')
        tk.Label(details_frame, text=f"Tarih: {entry['date']}\nBaşlık: {title}", font=font, bg='#FFFACD', fg='#4B0082').pack(pady=10)
        tk.Label(details_frame, text=entry['entry'], wraplength=350, bg='#FFFACD', fg='#4B0082', font=font).pack(pady=10)
        
        back_button = tk.Button(details_frame, text="Geri", command=show_past_entries, bg='#F0E68C', fg='#00008B', font=font)
        back_button.pack(side='bottom', anchor='e', padx=10, pady=10)
        
        show_frame(details_frame)

# Zaman kapsüllerini göstermek için fonksiyon
def show_time_capsules():
    time_capsules_frame = tk.Frame(main_frame, bg='#FFFACD')  # Limon Şifonu rengi
    
    canvas = tk.Canvas(time_capsules_frame, bg='#FFFACD')
    scrollbar = tk.Scrollbar(time_capsules_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='#FFFACD')
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    try:
        with open("time_capsules.json", "r") as file:
            time_capsules = json.load(file)
    except FileNotFoundError:
        time_capsules = []
    
    if not time_capsules:
        capsules_label = tk.Label(scrollable_frame, text="Henüz hiçbir zaman kapsülü oluşturmadınız!", wraplength=350, bg='#FFFACD', fg='#4B0082', font=font)
        capsules_label.pack(pady=10)
    else:
        for index, capsule in enumerate(time_capsules):
            title = capsule.get('title', 'Başlıksız')
            open_date = capsule['open_date']
            status = "Açıldı" if open_date <= datetime.now().strftime("%Y-%m-%d") else "Açılacak"
            capsule_frame = tk.Frame(scrollable_frame, bg='#FFFACD')
            capsule_button = tk.Button(capsule_frame, text=f"Başlık: {title} ({status})", wraplength=350, bg='#FFFACD', fg='#4B0082', anchor='w', justify='left', command=lambda i=index: show_capsule_details(i), font=font)
            capsule_button.pack(side="left", fill='x', expand=True)
            delete_button = tk.Button(capsule_frame, text="Sil", bg='#DC143C', fg='#FFFFFF', command=lambda i=index: delete_capsule(i), font=font)
            delete_button.pack(side="right", padx=5)
            capsule_frame.pack(pady=5, fill='x')
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    back_button = tk.Button(time_capsules_frame, text="Geri", command=time_capsule, bg='#F0E68C', fg='#00008B', font=font)
    back_button.pack(side='bottom', anchor='e', padx=10, pady=10)
    
    show_frame(time_capsules_frame)

# Zaman kapsülünü silmek için fonksiyon
def delete_capsule(index):
    try:
        with open("time_capsules.json", "r") as file:
            time_capsules = json.load(file)
    except FileNotFoundError:
        time_capsules = []
    
    if 0 <= index < len(time_capsules):
        del time_capsules[index]
        with open("time_capsules.json", "w") as file:
            json.dump(time_capsules, file, indent=4)
        show_time_capsules()

# Zaman kapsülünün detaylarını göstermek için fonksiyon
def show_capsule_details(index):
    try:
        with open("time_capsules.json", "r") as file:
            time_capsules = json.load(file)
    except FileNotFoundError:
        time_capsules = []
    
    if 0 <= index < len(time_capsules):
        capsule = time_capsules[index]
        current_date = datetime.now().strftime("%Y-%m-%d")

        details_frame = tk.Frame(main_frame, bg='#FFFACD')

        if current_date < capsule['open_date']:
            message = f"Bu zaman kapsülü {capsule['open_date']} tarihine kadar açılamaz."
            tk.Label(details_frame, text=message, font=font, bg='#FFFACD', fg='#4B0082').pack(pady=10)
        else:
            title = capsule.get('title', 'Başlıksız')
            tk.Label(details_frame, text=f"Başlık: {title}", font=font, bg='#FFFACD', fg='#4B0082').pack(pady=10)
            tk.Label(details_frame, text=f"Mesaj: {capsule['message']}\nAçılma Tarihi: {capsule['open_date']}", wraplength=350, bg='#FFFACD', fg='#4B0082', font=font).pack(pady=10)
        
        back_button = tk.Button(details_frame, text="Geri", command=show_time_capsules, bg='#F0E68C', fg='#00008B', font=font)
        back_button.pack(side='bottom', anchor='e', padx=10, pady=10)
        
        show_frame(details_frame)

if __name__ == "__main__":
    username = get_username()
    if not username:
        username = input("Adınızı girin: ")
        save_username(username)
    
    root = tk.Tk()
    root.title("Günlük Uygulaması")
    root.geometry("800x600")
    font = tkfont.Font(family="Helvetica", size=12, weight="bold")
    
    menu_frame = tk.Frame(root, width=200, bg='#D8BFD8')  # Açık Mor rengi
    menu_frame.pack(side='left', fill='y')
    menu_title = tk.Label(menu_frame, text="Menü", font=("Helvetica", 16, "bold"), bg='#D8BFD8', fg='#FFFFFF')
    menu_title.pack(pady=10)
    
    main_frame = tk.Frame(root, bg='#E6E6FA')  # Lavanta rengi
    main_frame.pack(side='right', fill='both', expand=True)
    
    previous_frame = None
    
    diary_frame = tk.Frame(main_frame, bg='#FFFACD')  # Limon Şifonu rengi
    entry_label = tk.Label(diary_frame, text="Günlük Başlığı:", bg='#FFFACD', fg='#4B0082', font=font)
    entry_label.pack()
    entry_title = tk.Entry(diary_frame, width=60, font=font)
    entry_title.pack()
    entry_text_label = tk.Label(diary_frame, text="Günlük Yazınızı Girin:", bg='#FFFACD', fg='#4B0082', font=font)
    entry_text_label.pack()
    entry_text = tk.Text(diary_frame, height=20, width=60, font=font)
    entry_text.pack()
    save_button = tk.Button(diary_frame, text="Kaydet", command=save_entry, bg='#4682B4', fg='#FFFFFF', font=font)  # Çelik Mavi rengi
    save_button.pack(pady=10)
    past_entries_button = tk.Button(diary_frame, text="Geçmiş Günlükler", command=show_past_entries, bg='#4682B4', fg='#FFFFFF', font=font)
    past_entries_button.pack(pady=10)
    
    tk.Button(menu_frame, text="Günlük Yaz", command=show_diary_frame, bg='#D8BFD8', fg='#FFFFFF', font=font).pack(fill='x')
    tk.Button(menu_frame, text="Hatıra Canlandırıcı", command=recall_memory, bg='#D8BFD8', fg='#FFFFFF', font=font).pack(fill='x')
    tk.Button(menu_frame, text="Zaman Kapsülü", command=time_capsule, bg='#D8BFD8', fg='#FFFFFF', font=font).pack(fill='x')
    
    show_diary_frame()
    
    root.mainloop()
