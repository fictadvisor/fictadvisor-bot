import './configure';
import bot from './bot';
import server from './server';

server.listen(process.env.PORT, () => console.log(`Server was launched on ${process.env.PORT} port`));

bot.launch()
    .then(() => console.log('Bot was launched.'))
    .catch((e) => console.log(`Failed to start the bot: ${e}`));
    