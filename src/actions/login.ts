import { Context } from 'telegraf';
import api from '../api';
import { writeFile as _writeFile } from 'fs';
import { createHmac } from 'crypto';
import axios from 'axios';

const getImageKey = (id: number) => createHmac('sha256', process.env.SECRET ?? '42')
  .update(id.toString())
  .digest('hex');

const writeFile = (path: string, data: any) => new Promise<void>((resolve, reject) => _writeFile(path, data, {}, err => (err ? reject(err) : resolve())));

const getUserPhoto = async (ctx: Context) => {
  try {
    const { photos } = await ctx.telegram.getUserProfilePhotos(ctx.from.id, 0, 1);

    if (photos.length === 0 || photos[0].length === 0) {
      return null;
    }

    const photo = photos[0][0];
    const url = await ctx.telegram.getFileLink(photo.file_id);

    const file = `images/${getImageKey(ctx.from.id)}.jpg`;
    const imagePath = `${process.env.STATIC_DIR}/${file}`;
    const { data } = await axios.get(url.toString(), { responseType: 'arraybuffer' });

    await writeFile(imagePath, data);

    return `/cdn/${file}`;
  } catch (e) {
    console.error(`Failed to fetch image for user (${ctx.from.id}): ${e}`);

    return null;
  }
};

export default () => async (ctx: Context) => {
  const { from } = ctx;

  try {
    const image = await getUserPhoto(ctx);

    const { data } = await api.oauth.telegram({
      telegram_id: from.id,
      first_name: from.first_name,
      last_name: from.last_name,
      username: from.username,
      image
    });

    const url = `${process.env.FRONT_BASE_URL}/oauth?access_token=${data.access_token}&refresh_token=${data.refresh_token}`;

    await ctx.reply(
      '<b>Авторизація на сайті <a href="https://fictadvisor.com">fictadvisor.com</a></b>\n\n' +
                'Ми не передаємо і не будемо ніколи передавати твої дані.\n' +
                'Вони використовуються лише в межах авторизації та ідентифікації нашої системи.\n\n' +
                `<b>Якщо кнопка не працює, тицьни <a href="${url}">сюди</a>.</b>`, {
        parse_mode: 'HTML',
        disable_web_page_preview: true,
        reply_markup: {
          inline_keyboard: [
            [{ text: 'Авторизуватись', url }],
            [{ text: 'Відмінити', callback_data: 'cancel_login' }]
          ]
        }
      });
  } catch (e) {
    console.error(`Authorization failed (${from.first_name}, ${from.id}): ${e}`);

    await ctx.reply('<b>На жаль, наразі наші сервіси недоступні.\nСпробуй авторизуватись через декілька хвилин.</b>\n\n/login', { parse_mode: 'HTML' });
  }
};
