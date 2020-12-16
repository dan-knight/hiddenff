export const testColumns = [
  { name: 'name', func: d => `${d.first} ${d.last}`, sortable: true, sortValue: 'last' },
  { name: 'position' },
  { name: 'team', func: d => d.team_id || '-' },
  { name: 'total_rush_yd', label: 'Rush Yd', sortable: true},
  { name: 'total_rec_yd', label: 'Rec Yd', sortable: true },
  { name: 'total_pass_yd', label: 'Pass Yd', sortable: true }
];

const playerName =  { name: 'name', label: 'Name', func: d => `${d.first} ${d.last}`, sortable: true, sortValue: 'last' };
const position =  { name: 'position', label: 'Position'};
const playerTeam = { name: 'team', label: 'Team', func: d => d.team_id || '-' };

const totalRushAtt = { name: 'total_rush_att', label: 'Rush Att', sortable: true };
const totalRushYd = { name: 'total_rush_yd', label: 'Rush Yd', sortable: true };
const totalRushTD = { name: 'total_rush_td', label: 'Rush TD', sortable: true };
const totalRushYdPerAtt = { name: 'total_rush_yd_per_att', label: 'Rush Yd Per Att', sortable: true };

const totalTgt = { name: 'total_tgt', label: 'Targets', sortable: true };
const totalRec = { name: 'total_rec', label: 'Rec', sortable: true };
const totalRecYd = { name: 'total_rec_yd', label: 'Rec Yd', sortable: true };
const totalRecTD = { name: 'total_rec_td', label: 'Rec TD', sortable: true };
const totalRecYdPerRec = { name: 'total_rec_yd_per_rec', label: 'Rec Yd Per Rec', sortable: true };

const totalPassAtt = { name: 'total_pass_att', label: 'Pass Att', sortable: true };
const totalPassCmp = { name: 'total_pass_cmp', label: 'Pass Cmp', sortable: true };
const totalPassYd = { name: 'total_pass_yd', label: 'Pass Yd', sortable: true };
const totalPassTD = { name: 'total_pass_td', label: 'Pass TD', sortable: true };
const totalPassYdPerCmp = { name: 'total_pass_yd_per_cmp', label: 'Pass Yd Per Cmp', sortable: true };



const rushColumns = [totalRushAtt, totalRushYd, totalRushTD, totalRushYdPerAtt];
const recColumns = [totalTgt, totalRec, totalRecYd, totalRecTD, totalRecYdPerRec]
const passColumns = [totalPassYd];

const playerOverviewColumns = {
  basic: [playerName, position, playerTeam],
  all: [rushColumns, recColumns, passColumns],
  QB: [rushColumns, passColumns],
  RB: [rushColumns, recColumns],
  WR: [recColumns],
  TE: [recColumns]
};

export const columns = {
  playerOverview: playerOverviewColumns
};





