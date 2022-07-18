import { AxiosInstance } from 'axios';

type UpdateSubjectPayload = {
    name?: string;
    description?: string;
    state?: 'pending' | 'approved' | 'declined';
};

export default (client: AxiosInstance) => {
  const update = (id: string, payload: UpdateSubjectPayload) => client.put(`/subjects/${id}`, payload);
  const deleteSubject = (id: string) => client.delete(`/subjects/${id}`);

  return {
    update,
    delete: deleteSubject
  };
};
