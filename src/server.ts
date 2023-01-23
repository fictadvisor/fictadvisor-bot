import express from 'express';
import cors from 'cors';
import routes from './api/v1/index';

const server = express();

server.use(cors());
server.use(express.json());

server.use('/api/v1', routes);

export default server;
