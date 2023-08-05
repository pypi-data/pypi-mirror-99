from abc import ABC
from collections import defaultdict
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from negmas import AgentMechanismInterface
from negmas import Mechanism
from negmas import MechanismState
from negmas.negotiators import Negotiator
from negmas.outcomes import Issue
from negmas.situated import Agent
from negmas.situated import Breach
from negmas.situated import Contract
from negmas.situated import RenegotiationRequest

from .agent import SCML2019Agent
from .common import Factory
from .common import InsurancePolicy

if TYPE_CHECKING:
    from .world import SCML2019World

__all__ = ["DefaultInsuranceCompany", "InsuranceCompany"]


class InsuranceCompany(Agent, ABC):
    """Base class for all insurance companies"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._world: Optional[SCML2019World] = None

    def _respond_to_negotiation_request(
        self,
        initiator: str,
        partners: List[str],
        issues: List[Issue],
        annotation: Dict[str, Any],
        mechanism: AgentMechanismInterface,
        role: Optional[str],
        req_id: Optional[str],
    ) -> Optional[Negotiator]:
        pass

    def on_neg_request_rejected(self, req_id: str, by: Optional[List[str]]):
        pass

    def on_neg_request_accepted(self, req_id: str, mechanism: AgentMechanismInterface):
        pass

    def on_negotiation_failure(
        self,
        partners: List[str],
        annotation: Dict[str, Any],
        mechanism: AgentMechanismInterface,
        state: MechanismState,
    ) -> None:
        pass

    def on_negotiation_success(
        self, contract: Contract, mechanism: AgentMechanismInterface
    ) -> None:
        pass

    def on_contract_signed(self, contract: Contract) -> None:
        pass

    def on_contract_cancelled(self, contract: Contract, rejectors: List[str]) -> None:
        pass

    def sign_contract(self, contract: Contract) -> Optional[str]:
        pass

    def respond_to_negotiation_request(
        self,
        initiator: str,
        partners: List[str],
        issues: List[Issue],
        annotation: Dict[str, Any],
        mechanism: Mechanism,
        role: Optional[str],
        req_id: str,
    ) -> Optional[Negotiator]:
        pass

    def on_contract_breached(
        self, contract: Contract, breaches: List[Breach], resolution: Optional[Contract]
    ) -> None:
        pass

    def on_contract_executed(self, contract: Contract) -> None:
        pass


class DefaultInsuranceCompany(InsuranceCompany):
    """Represents an insurance company in the world"""

    def __init__(
        self,
        premium: float,
        premium_breach_increment: float,
        premium_time_increment: float,
        a2f: Dict[str, Factory],
        disabled=False,
        name: str = None,
    ):
        super().__init__(name=name)
        self.premium_breach_increment = premium_breach_increment
        self.premium = premium
        self.disabled = disabled
        self.premium_time_increment = premium_time_increment
        self.insured_contracts: Dict[Tuple[Contract, str], InsurancePolicy] = dict()
        self.storage: Dict[int, int] = defaultdict(int)
        self.wallet: float = 0.0
        self.a2f = a2f

    def init(self):
        pass

    def set_renegotiation_agenda(
        self, contract: Contract, breaches: List[Breach]
    ) -> Optional[RenegotiationRequest]:
        return None

    def respond_to_renegotiation_request(
        self, contract: Contract, breaches: List[Breach], agenda: RenegotiationRequest
    ) -> Optional[Negotiator]:
        raise ValueError("The insurance company does not receive callbacks")

    def evaluate_insurance(
        self,
        contract: Contract,
        insured: SCML2019Agent,
        against: SCML2019Agent,
        t: int = None,
    ) -> Optional[float]:
        """Can be called to evaluate the premium for insuring the given contract against breaches committed by others

        Args:

            against: The `SCML2019Agent` to insure against
            contract: hypothetical contract
            insured: The `SCML2019Agent` to buy the insurance
            t: time at which the policy is to be bought. If None, it means current step

        Remarks:

            - The premium returned is relative to the contract price. To actually calculate the cost of buying this
              insurance, you need to multiply this by the contract value (quantity * unit_price).

        """
        if self.disabled:
            return None
        # fail if no premium
        if self.premium is None:
            return None

        # assume the insurance is to be bought now if needed
        if t is None:
            t = self.awi.current_step

        # find the delay from contract signing. The more this is the more expensive the insurance will be
        if contract.signed_at is None:
            dt = 0
        else:
            dt = max(0, t - contract.signed_at)

        # fail if the insurance is to be bought at or after the agreed upon delivery time
        if t >= contract.agreement.get("time", -1):
            return None

        # find the total breach of the agent I am insuring against. The more this is, the more expensive the insurance
        breaches = self.awi.bb_query(section="breaches", query={"perpetrator": against})
        b = 0
        if breaches is not None:
            for _, breach in breaches.items():
                b += breach.level
        return (self.premium + b * self.premium_breach_increment) * (
            1 + self.premium_time_increment * dt
        )

    def buy_insurance(
        self, contract: Contract, insured: SCML2019Agent, against: SCML2019Agent
    ) -> Optional[InsurancePolicy]:
        """Buys insurance for the contract at the premium calculated by the insurance company.

        Remarks:
            The agent can call `evaluate_insurance` to find the premium that will be used.

        See Also:

            `evaluate_premium`

        """
        if self.disabled:
            return None
        premium = self.evaluate_insurance(
            contract=contract, t=self.awi.current_step, insured=insured, against=against
        )
        if premium is None:
            return None

        premium *= contract.agreement["quantity"] * contract.agreement["unit_price"]

        factory = self.a2f[insured.id]
        if factory.wallet < premium:
            return None
        factory.pay(premium)
        self.wallet += premium
        policy = InsurancePolicy(
            contract=contract,
            at_time=self.awi.current_step,
            against=against,
            premium=premium,
        )
        self.insured_contracts[(contract, against.id)] = policy
        return policy

    def is_insured(self, contract: Contract, perpetrator: SCML2019Agent) -> bool:
        """

        Args:
            contract:
            perpetrator:

        Returns:

        """
        if self.disabled:
            return False
        if (contract, perpetrator.id) in self.insured_contracts.keys():
            del self.insured_contracts[(contract, perpetrator.id)]
            return True
        return False

    def step(self):
        """does nothing"""
