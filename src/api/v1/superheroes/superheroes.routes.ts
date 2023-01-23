import { Router } from 'express';
import { SuperheroesController } from './superheroes.controller';

const router = Router();

router.route('/broadcastPending').post(SuperheroesController.broadcastPending);

export default router;