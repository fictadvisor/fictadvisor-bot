import { AxiosInstance } from "axios";

type UpdateContactPayload = {
    state?: 'pending' | 'approved' | 'declined';
    name?: string;
    value?: string;
};

export default (client: AxiosInstance) => {
    const update = (id: string, payload: UpdateContactPayload) => client.put(`/teachers/contacts/${id}`, payload);
    const deleteContact = (id: string) => client.delete(`/teachers/contacts/${id}`);

    return {
        update,
        delete: deleteContact,
    };
};
