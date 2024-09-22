const ValuCoin = artifacts.require('ValuCoin');

module.exports = function(deployer) {
    deployer.deploy(ValuCoin);
}
