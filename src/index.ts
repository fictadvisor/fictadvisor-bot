import './configure';
import bot from './bot';
import { existsSync, mkdirSync } from 'fs';

// import server from './server';

// server.listen(process.env.PORT, () => console.log(`Server was launched on ${process.env.PORT} port`));

const staticPaths = ['/images'];

for (const path of staticPaths) {
  const fullPath = `${process.env.STATIC_DIR}${path}`;

  if (existsSync(fullPath)) {
    continue;
  }

  mkdirSync(fullPath, { recursive: true });
}

bot.launch()
  .then(() => console.log('Bot was launched.'))
  .catch(e => console.log(`Failed to start the bot: ${e}`));
