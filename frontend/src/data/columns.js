export const playerColumns = () => ({
  // Basic
  name: { label: 'Name' },
  position: { label: 'Position', unsortable: true },
  team: { label: 'Team', func: d => d.team ?? '-', unsortable: true },
  // 
  // Passing
  total_pass_att: { label: 'Pass Att' },
  total_pass_cmp: { label: 'Pass Cmp' },
  total_pass_yd: { label: 'Pass Yds' },
  total_pass_td: { label: 'Pass TDs' },
  total_pass_yd_per_cmp: { label: 'Pass Yd / Cmp', decimal: true },
  // 
  // Rushing
  total_rush_att: { label: 'Rush Att' },
  total_rush_yd: { label: 'Rush Yards' },
  total_rush_td: { label: 'Rush TDs' },
  total_rush_yd_per_att: { label: 'Rush Yd / Att', decimal: true },
  // 
  // Receiving
  total_tgt: { label: 'Targets' },
  total_rec: { label: 'Rec' },
  total_rec_yd: { label: 'Rec Yards' },
  total_rec_td: { label: 'Rec TDs' },
  total_rec_yd_per_rec: { label: 'Rec Yd / Rec', decimal: true },
});




