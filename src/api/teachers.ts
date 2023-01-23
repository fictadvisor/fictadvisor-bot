import { AxiosInstance } from 'axios';

type UpdateTeacherPayload = {
    state?: 'pending' | 'approved' | 'declined';
    firstName?: string;
    lastName?: string;
    middleName?: string;
    description?: string;
};

export default (client: AxiosInstance) => {
  const update = (id: string, payload: UpdateTeacherPayload) => client.put(`/teachers/${id}`, payload);
  const deleteTeacher = (id: string) => client.delete(`/teachers/${id}`);

  return {
    update,
    delete: deleteTeacher,
  };
};
