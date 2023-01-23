import { SuperheroesService } from './superheroes.service';

export class SuperheroesController {
  static async broadcastPending(req, res) {
    try {
      const data = SuperheroesService.broadcastPending(req.body);
      return res.status(200).send({message: data});
    } catch(err) {
      return res.status(400).send({message: 'An exception occured while sending message'});
    }
  }
}