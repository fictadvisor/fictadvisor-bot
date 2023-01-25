import { State } from './state';
import { client } from './index';

type UpdateSuperheroPayload = {
    state?: keyof typeof State;
};

export class SuperheroAPI {
  static async update (id: string, payload: UpdateSuperheroPayload) {
    return (await client.patch(`/superheroes/${id}`, payload)).data;
  }
}
