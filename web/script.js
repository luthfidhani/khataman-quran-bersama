window.app = {
    periods: [],
    members: [],
    detailPeriod: [],
    alert: '',
    loading: true,
    selectedMemberId: '',
    selectedMemberName: '',
    newMemberName: '',
    memberNameUpdate: '',
    api: 'https://khataman-quran-bersama.onrender.com',
    // api: 'http://localhost:8000',

    fetchData(endpoint, method = 'GET', body = null) {
        this.loading = true;
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Internal-Call': true
            }
        };

        if (body) {
            options.body = JSON.stringify(body);
        }

        return fetch(this.api + endpoint, options)
            .then(async (resp) => {
                this.loading = false;
                if (resp.ok) {
                    return resp.json();
                } else {
                    this.alert = await resp.text();
                    return null;
                }
            });
    },

    loadMembers() {
        this.fetchData('/member/').then(data => {
            if (data) {
                this.members = data;
            } else {
                this.members = [];
            }
        });
    },

    loadPeriods() {
        this.fetchData('/period/').then(data => {
            if (data) {
                this.periods = data;
            } else {
                this.periods = [];
            }
        });
    },

    loadChecklist(period = 'current') {
        this.fetchData(`/period/${period}`).then(data => {
            if (data) {
                this.detailPeriod = data;
                this.detailPeriod.data.sort((a, b) => a[0].name.localeCompare(b[0].name));
            } else {
                this.detailPeriod = [];
            }
        });
    },

    addMember() {
        this.fetchData('/member/', 'POST', { name: this.newMemberName }).then(() => {
            this.loadMembers();
        });
    },

    updateMember() {
        const data = {
            id: this.selectedMemberId,
            update: { name: this.memberNameUpdate }
        };
        this.fetchData('/member/', 'PUT', data).then(() => {
            this.loadMembers();
        });
    },

    deleteMember(id) {
        this.fetchData('/member/', 'DELETE', { id: id }).then(() => {
            this.loadMembers();
        });
    },

    createPeriod() {
        const payload = {
            name: document.querySelector('#input-period').value,
            data: this.members.map(member => {
                const juzRange = document.querySelector(`#input_juz${member.id}`).value;
                let juzArray = [];
                if (juzRange.includes('-')) {
                    const [start, end] = juzRange.split('-').map(Number);
                    for (let i = start; i <= end; i++) {
                        juzArray.push(i);
                    }
                } else {
                    juzArray.push(Number(juzRange));
                }

                return {
                    "id": document.querySelector(`#input_member_id${member.id}`).value,
                    "juz": juzArray
                };
            })
        };

        this.fetchData('/period/', 'POST', payload).then(() => {
            this.loadPeriods();
        });
    },

    updateChecklist(period) {
        const payload = {
            data: this.detailPeriod.data.map(checklist => [
                {
                    "name": document.querySelector(`#member_name${checklist[0].id}`).value,
                    "id": document.querySelector(`#member_id${checklist[0].id}`).value
                },
                {
                    "juz": checklist[1].juz.map(juzItem => ({
                        "number": document.querySelector(`#juz_number${juzItem.number}`).value,
                        "status": document.querySelector(`#juz_status${juzItem.number}`).checked
                    }))
                }
            ])
        };

        this.fetchData(`/period/${period}`, 'PUT', payload).then(() => {
            this.loadChecklist(period);
        });
    },

    lockPeriod(period) {
        this.fetchData(`/period/${period}/lock`).then(() => {
            this.loadChecklist(period);
        });
    }
}
