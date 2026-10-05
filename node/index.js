const { SlippiGame } = require('@slippi/slippi-js/node');
const fss = require('fs');
const fs = require('fs/promises');
const path = require('path');

const slippiFiles = [];
const slippiDir = '../SlippiFiles/';

function recurseDir(dir) {
  fss.readdirSync(dir, { withFileTypes: true }).forEach(f => {
    const p = path.join(dir, f.name);
    if (f.isDirectory()) recurseDir(p);
    else slippiFiles.push(p);
  });
}
recurseDir(slippiDir);

(async function() {
  const out = fss.createWriteStream('./games.csv');
  
  out.write('player character,opponent character,win,player stocks,opponent stocks,player final damage,opponent final damage,player total damage,opponent total damage,player openings,player kills,opponent openings,opponent kills,player neutral wins,opponent neutral wins,total neutral breaks,stage,match length\n');

  const done = slippiFiles.map(async p => {
    const buf = await fs.readFile(p);
    const game = new SlippiGame(buf);

    if (game.getSettings().isTeams) return;

    const metadata = game.getMetadata();
    if (!metadata) return;

    const players = metadata.players;
    if (!players) return;

    const self0 = players['0']?.names?.code === 'CABL#298';
    const self1 = players['1']?.names?.code === 'CABL#298';
    if (!self0 && !self1) return;

    const self = self0 ? '0' : '1';
    const oppo = self0 ? '1' : '0';
    
    const selfCharacter = Object.entries(players[self].characters).sort((a, b) => b[1] - a[1])[0][0];
    const oppoCharacter = Object.entries(players[oppo].characters).sort((a, b) => b[1] - a[1])[0][0];

    out.write(selfCharacter + ',');
    out.write(oppoCharacter + ',');

    const didWin = game.getWinners()[0].playerIndex == self;

    out.write(didWin ? '1' : '0');
    out.write(',');

    const selfLastStock = game.getStats().stocks.toReversed().find(v => v.playerIndex == self);
    const oppoLastStock = game.getStats().stocks.toReversed().find(v => v.playerIndex == oppo);

    let selfStocks = selfLastStock.count;
    let oppoStocks = oppoLastStock.count;
    let selfDamage = selfLastStock.currentPercent;
    let oppoDamage = oppoLastStock.currentPercent;

    if (selfLastStock.endFrame) {
      selfStocks--;
      selfDamage = 0;
    }
    if (oppoLastStock.endFrame) {
      oppoStocks--;
      oppoDamage = 0;
    }

    out.write(selfStocks + ',');
    out.write(oppoStocks + ',');
    out.write(selfDamage + ',');
    out.write(oppoDamage + ',');

    const selfOverall = game.getStats().overall.find(v => v.playerIndex == self);
    const oppoOverall = game.getStats().overall.find(v => v.playerIndex == oppo);

    out.write(selfOverall.totalDamage + ',');
    out.write(oppoOverall.totalDamage + ',');
    out.write(selfOverall.openingsPerKill.count + ',');
    out.write(selfOverall.openingsPerKill.total + ',');
    out.write(oppoOverall.openingsPerKill.count + ',');
    out.write(oppoOverall.openingsPerKill.total + ',');
    out.write(selfOverall.neutralWinRatio.count + ',');
    out.write(oppoOverall.neutralWinRatio.count + ',');
    out.write(selfOverall.neutralWinRatio.total + ',');
    if (selfOverall.neutralWinRatio.total !== oppoOverall.neutralWinRatio.total) console.log('sadness');

    const stage = game.getSettings().stageId;
    out.write(stage + ',');

    const lastFrame = metadata.lastFrame;
    out.write((lastFrame ?? -1).toString());

    out.write('\n');
  });

  await Promise.allSettled(done);
  out.close();
}());