import './configure';
import app from './app';

app.launch()
    .then(() => console.log('Bot was launched.'))
    .catch((e) => console.log(`Failed to start the bot: ${e}`));
    