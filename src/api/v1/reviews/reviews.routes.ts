import { Router } from 'express';
import { ReviewsController } from './reviews.controller';

const router = Router();

router.route('/broadcastPending').post(ReviewsController.broadcastPending)

export default router;