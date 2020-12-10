export const columns = [
  { name: 'name', func: d => `${d.first} ${d.last}`, sortable: true, sortValue: 'last' },
  { name: 'position' },
  { name: 'team', func: d => d.team_id || '-' },
  { name: 'total_rush_yd', label: 'Rush Yd', sortable: true},
  { name: 'total_rec_yd', label: 'Rec Yd', sortable: true },
  { name: 'total_pass_yd', label: 'Pass Yd', sortable: true }
];