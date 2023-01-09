import { ReviewsService } from './reviews.service';

export class ReviewsController {
    static async broadcastPending(req, res) {
        try {
            const data = ReviewsService.broadcastPending(req.body);
            return res.status(200).send({message: data});
        } catch(err) {
            return res.status(400).send({message: 'An exception occured while sending message'});
        }
    }
}