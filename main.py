import instaloader
import os

# Desktop'a geçiş
os.chdir("C:/Users/PcUser/Desktop")
bot = instaloader.Instaloader()

profile_name = input("Lütfen indirmek istediğiniz hesabı girin: ")

# Kullanıcı adını kontrol et
try:
    profile = instaloader.Profile.from_username(bot.context, profile_name)
except instaloader.exceptions.ProfileNotExistsException:
    print(f"üzgünüz... {profile_name} kullanıcı adıyla bir hesap bulunmuyor.Lütfen geçerli bir kullanıcı adı girin.")
    exit()
except instaloader.exceptions.ConnectionException:
    print("Bağlantınızda sorun oluştu.Lütfen internet bağlantınızı kontrol edip tekrar deneyin.")
    exit()

while True:
# Hesap özel mi kontrol et
   if profile.is_private:
       print(f"\nBu hesap gizli. Yalnızca profil fotoğrafını indirebilir ya da {profile_name} olarak giriş yapıp bütün içerikleri indirebilirsin!")
       choice = input("Lütfen bir seçim yapın:\n 1) GİRİŞ YAP\n 2) YALNIZCA PROFİL FOTOĞRAFINI İNDİR\n 3) ÇIKIŞ YAP\n")

       if choice == "1":
           target_username = input("Giriş yapmak için kullanıcı adınızı girin: ")
           password = input(f" {profile_name} adlı hesaba ait şifre:\n")
           print("Giriş yapılıyor...")
           try:
               bot.login(user=profile_name, passwd=password)
               print(f"\nBaşarılı bir şekilde giriş yapıldı. Hoşgeldin {profile_name}!")

               while True:
                   user_action = input("Yapmak istediğiniz eylemi seçin.\n (G) Gönderiler - (H) Hikayeler - (+) Tüm Gönderiler ve Hikayeler:\n").upper()

                   if user_action == "G":
                       print(f" {profile_name}'ın bütün fotoğrafları indiriliyor...")
                       bot.download_profile(profile_name, profile_pic_only=False)  # Resimleri indir
                       break  # İndirdikten sonra döngüden çık

                   elif user_action == "H":
                       print(f" {profile_name}'ın son 24 saatteki bütün hikayeleri indiriiyor...")
                       for story in bot.get_stories(userids=[profile.userid]):
                           for item in story.get_items():
                               bot.download_storyitem(item, target=profile.username)

                   elif user_action == "+":
                       print(f" {profile_name}'ın bütün gönderileri ve hikayeleri indriliyor...")
                       for story in bot.get_stories(userids=[profile.userid]):
                           for item in story.get_items():
                               bot.download_storyitem(item, target=profile.username)
                       bot.download_profile(profile_name, profile_pic_only=False)
                       break

                   else:
                       print("Geçersiz karakter. Lütfen verilen seçeneklerden birini seçin.\n(F/G/+)")

           except instaloader.exceptions.BadCredentialsException:
               print("Yanlış şifre.Tekrar deneyin.")
               exit()
           except instaloader.exceptions.ConnectionException:
               print("Giriş yapılırken bağlantı sorunu oluştu.Lütfen tekrar deneyin.")
               exit()

       elif choice == "2":
           print(f"{profile_name}'ın profil fotoğrafı indiriliyor...")
           bot.download_profile(profile_name, profile_pic_only=True)
       elif choice == "3":
           print("Öptüm say,gömdüm bay!")
       else:
           print("Geçersiz karakter.Lütfen seçeneklerden birini seçin.\n(1/2/3)")

   else:
       print(f" {profile_name}'ın bütün gönderileri indiriliyor...")
       bot.download_profile(profile_name, profile_pic_only=False)


