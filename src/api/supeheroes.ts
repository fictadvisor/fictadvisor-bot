import { AxiosInstance } from 'axios';

type UpdateSuperheroPayload = {
    state?: 'pending' | 'approved' | 'hidden';
};

export default (client: AxiosInstance) => {
  const update = (id: string, payload: UpdateSuperheroPayload) => client.put(`/superheroes/${id}`, payload);

  return {
    update
  };
};
