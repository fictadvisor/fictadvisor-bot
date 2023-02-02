import { client } from './index';

export class UserAPI {
  static async verifyStudent(id: string, state: string) {
    await client.patch(`/users/${id}/verifyStudent`, {state});
  }

  static async verifySuperhero(id: string, state: string) {
    await client.patch(`/users/${id}/verifySuperhero`, {state});
  }

  static async getUser(id: string) {
    const { data } = await client.patch(`/users/${id}/telegram`);
    return data;
  }
}