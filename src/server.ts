import express from 'express';
import cors from 'cors';
import routes from './api/v1/index';
import * as process from "process";

const server = express();

server.use(cors());
server.use(express.json());

server.use(function (req, res, next) {
  try {
    const token = req.headers.authorization.split(" ")[1];
    if (token != process.env.BOT_TOKEN) {
      res.status(401).json({
        message: 'Unauthorized',
      });
    } else {
      next();
    }
  } catch {
    res.status(401).json({
      message: 'Unauthorized',
    });
  }
});

server.use('/api/v1', routes);

export default server;
