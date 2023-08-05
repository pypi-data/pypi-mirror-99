from contracts_lib_py.conditions.condition_base import ConditionBase


class LockPaymentCondition(ConditionBase):
    """Class representing the LockPaymentCondition contract."""
    CONTRACT_NAME = 'LockPaymentCondition'

    def fulfill(self, agreement_id, did, reward_address, amounts, receivers, account):
        """
        Fulfill the lock reward condition.

        :param agreement_id: id of the agreement, hex str
        :param did: id of the asset, hex str
        :param reward_address: the contract address where the reward is locked, hex str
        :param amounts: Array of amount of tokens to distribute, int[]
        :param receivers: Array of ethereum address of the receivers, hex str[]
        :param account: Account instance
        :return:
        """
        return self._fulfill(
            agreement_id,
            did,
            reward_address,
            amounts,
            receivers,
            transact={'from': account.address,
                      'passphrase': account.password,
                      'keyfile': account.key_file}
        )

    def hash_values(self, did, reward_address, amounts, receivers):
        """
        Hash of the values of the lock reward condition.

        :param did: id of the asset, hex str
        :param reward_address: the contract address where the reward is locked, hex str
        :param amounts: Array of amount of tokens to distribute, int[]
        :param receivers: Array of ethereum address of the receivers, hex str[]
        :return: hex str
        """
        return self._hash_values(
            did,
            reward_address,
            amounts,
            self.to_checksum_addresses(receivers)
        )
