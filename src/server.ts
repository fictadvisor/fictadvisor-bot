import express from 'express';
import cors from 'cors';
import proxy from './routes/proxy';

const server = express();

server.use(cors());
server.use(express.json());

server.get('/proxy', proxy());

export default server;
