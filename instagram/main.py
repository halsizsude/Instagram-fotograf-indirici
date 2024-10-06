from flask import Flask, render_template, request, redirect, url_for, flash
import instaloader
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Güvenlik için gerekli


# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')


# Kullanıcı profili indirme
@app.route('/download', methods=['POST'])
def download():
    profile_name = request.form['profile_name']
    bot = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(bot.context, profile_name)
    except instaloader.exceptions.ProfileNotExistsException:
        flash(
            f"Üzgünüz... {profile_name} kullanıcı adıyla bir hesap bulunmuyor. Lütfen geçerli bir kullanıcı adı girin.")
        return redirect(url_for('index'))
    except instaloader.exceptions.ConnectionException:
        flash("Bağlantınızda sorun oluştu. Lütfen internet bağlantınızı kontrol edip tekrar deneyin.")
        return redirect(url_for('index'))

    # Eğer profil özel ise, seçenekleri göster
    if profile.is_private:
        return render_template('private_profile.html', profile_name=profile_name)
    else:
        # Profil fotoğrafı ve gönderileri indir
        bot.download_profile(profile_name, profile_pic_only=False)
        flash(f"{profile_name} adlı kullanıcının gönderileri indirildi.")
        return redirect(url_for('index'))


# Ana sayfada profil fotoğrafı indirme işlemi
@app.route('/download_private', methods=['POST'])
def download_private():
    profile_name = request.form['profile_name']
    username = request.form['username']
    password = request.form['password']

    bot = instaloader.Instaloader()

    try:
        bot.login(user=username, passwd=password)
        bot.download_profile(profile_name, profile_pic_only=False)
        flash(f"{profile_name} adlı kullanıcının gönderileri indirildi.")
    except instaloader.exceptions.BadCredentialsException:
        flash("Yanlış şifre. Tekrar deneyin.")
    except instaloader.exceptions.ConnectionException:
        flash("Giriş yapılırken bağlantı sorunu oluştu. Lütfen tekrar deneyin.")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
